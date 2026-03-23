mapred streaming \
 -files src/mapper_task4.py,src/reducer_sum.py \
 -mapper "python3 mapper_task4.py" \
 -reducer "python3 reducer_sum.py" \
 -input /data/chicago_crimes.csv \
 -output /user/mhussen/project/m1/task4