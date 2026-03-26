mapred streaming \
-files src/mapper_task5.py,src/reducer_sum.py \
-mapper "python3 mapper_task5.py" \
-reducer "python3 reducer_sum.py" \
-input /data/chicago_crimes.csv \
-output /user/YOUR_CLUSTER_USERNAME/project/m1/task5