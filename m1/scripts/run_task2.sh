mapred streaming \
-files src/mapper_task2.py,src/reducer_sum.py \
-mapper "python3 mapper_task2.py" \
-reducer "python3 reducer_sum.py" \
-input /data/chicago_crimes.csv \
-output /user/fkhalil/project/m1/task2
