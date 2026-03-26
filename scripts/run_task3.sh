mapred streaming \
   -files src/mapper_task3.py,src/reducer_sum.py \
   -mapper "python3 mapper_task3.py" \ 
   -reducer "python3 reducer_sum.py" \ 
   -input /data/chicago_crimes.csv \ 
   -output /user/tanalam/project/m1/task3