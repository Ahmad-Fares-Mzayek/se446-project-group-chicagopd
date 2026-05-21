# ============================================
# SE446 - Milestone 2: Spark ML Pipeline
# Group ChicagoPD
#
# Tasks 5-6: Mohammad Ghassan Hussen (ID: 230367)
# Task 7:    Bilal Othman (ID: 230031)
# Adapted for spark-submit by: Ahmad Fares Mzayek (ID: 230695)
# ============================================

import time
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, hour, to_timestamp
from pyspark.ml import Pipeline
from pyspark.ml.feature import StringIndexer, VectorAssembler
from pyspark.ml.classification import (
    LogisticRegression, RandomForestClassifier, GBTClassifier,
)
from pyspark.ml.evaluation import (
    BinaryClassificationEvaluator, MulticlassClassificationEvaluator,
)


def main():
    spark = (
        SparkSession.builder
        .appName("SE446_M2_ChicagoPD_SparkSubmit")
        .getOrCreate()
    )
    spark.sparkContext.setLogLevel("WARN")

    print("=" * 60)
    print("M2 Phase B: ML Pipeline (Tasks 5-7) via spark-submit")
    print("=" * 60)

    # ----- Load data + extract Hour from Date column -----
    df = spark.read.csv(
        "hdfs:///data/chicago_crimes.csv",
        header=True, inferSchema=True,
    )
    df = df.withColumn(
        "Hour", hour(to_timestamp(col("Date"), "MM/dd/yyyy hh:mm:ss a"))
    )
    # Sample per spec hint to fit cluster's small memory budget
    df = df.sample(0.05, seed=42)

    # ----- Clean: cast label and dropna -----
    df_ml = (
        df.withColumn("label", col("Arrest").cast("integer"))
          .withColumn("Domestic_str", col("Domestic").cast("string"))
          .dropna(subset=["Primary Type", "Domestic_str", "District", "Hour", "label"])
    )
    print(f"Training data (sampled 5%): {df_ml.count():,} rows")

    # ----- Task 5: feature pipeline -----
    crime_indexer = StringIndexer(
        inputCol="Primary Type", outputCol="crime_index", handleInvalid="skip"
    )
    domestic_indexer = StringIndexer(
        inputCol="Domestic_str", outputCol="domestic_index", handleInvalid="skip"
    )
    assembler = VectorAssembler(
        inputCols=["District", "crime_index", "Hour", "domestic_index"],
        outputCol="features",
    )
    feature_stages = [crime_indexer, domestic_indexer, assembler]

    train_df, test_df = df_ml.randomSplit([0.8, 0.2], seed=42)
    train_df.cache()
    print(f"Train: {train_df.count():,}  Test: {test_df.count():,}")

    # ----- Task 6: train + evaluate 3 models -----
    # maxBins=64 because Chicago crime data has ~33 distinct Primary Type
    # values; default 32 is insufficient
    models = {
        "Logistic Regression": LogisticRegression(maxIter=100, regParam=0.01),
        "Random Forest":       RandomForestClassifier(numTrees=100, maxDepth=5, seed=42, maxBins=64),
        "GBT":                 GBTClassifier(maxIter=50, maxDepth=5, seed=42, maxBins=64),
    }
    auc_eval = BinaryClassificationEvaluator(labelCol="label", metricName="areaUnderROC")
    acc_eval = MulticlassClassificationEvaluator(labelCol="label", metricName="accuracy")
    f1_eval  = MulticlassClassificationEvaluator(labelCol="label", metricName="f1")

    results = {}
    model_rf = None

    for name, classifier in models.items():
        print(f"\nTraining {name}...")
        pipeline = Pipeline(stages=feature_stages + [classifier])
        start = time.time()
        fitted = pipeline.fit(train_df)
        elapsed = time.time() - start

        preds = fitted.transform(test_df)
        auc = auc_eval.evaluate(preds)
        acc = acc_eval.evaluate(preds)
        f1  = f1_eval.evaluate(preds)
        results[name] = (auc, acc, f1, elapsed)

        if name == "Random Forest":
            model_rf = fitted

    print("\n" + "=" * 70)
    print(f"{'Model':<22} {'AUC':>8} {'Acc':>8} {'F1':>8} {'Time(s)':>10}")
    print("-" * 70)
    for name, (auc, acc, f1, t) in results.items():
        print(f"{name:<22} {auc:>8.4f} {acc:>8.4f} {f1:>8.4f} {t:>10.2f}")

    # ----- Task 7: feature importances -----
    rf = model_rf.stages[-1]
    feature_names = ["District", "crime_index", "Hour", "domestic_index"]
    print("\nRandom Forest feature importances:")
    for name, imp in sorted(
        zip(feature_names, rf.featureImportances.toArray()),
        key=lambda x: x[1], reverse=True,
    ):
        print(f"  {name:<20} {imp:.4f}")

    spark.stop()


if __name__ == "__main__":
    main()