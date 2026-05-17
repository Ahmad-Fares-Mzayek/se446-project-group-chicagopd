# SE446 Big Data Engineering — Group Project
## Chicago Crime Analytics

End-to-end big data analytics on the Chicago Crime dataset (2001–2025, ~793K records), evolving from batch MapReduce counting in Milestone 1 to in-memory Spark analytics and MLlib-based arrest prediction in Milestone 2.

---

## Team Members

| Name                    | Student ID |
|-------------------------|------------|
| Ahmad Fares Mzayek      | 230695     |
| Tanzim Alam             | 220693     |
| Mohammad Ghassan Hussen | 230367     |
| Faisal Hajj Khalil      | 230023     |
| Bilal Othman            | 230031     |

---

## Milestones

### [Milestone 1 — MapReduce on Hadoop](./m1/README.md)
Python MapReduce streaming pipeline on a 3-node Hadoop 3.4.1 cluster. Crime type distribution, location hotspots, year trends, and arrest analysis.

### [Milestone 2 — Spark + MLlib](./m2/README.md)
Spark DataFrame and SQL analytics reproducing M1 results, plus an end-to-end MLlib pipeline predicting arrest outcomes with Logistic Regression, Random Forest, and GBT classifiers. Deployed in three execution modes: local, YARN client, and spark-submit cluster.

---
