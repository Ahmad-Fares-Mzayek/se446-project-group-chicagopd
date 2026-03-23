# SE446 Big Data Engineering — Group Project
## Chicago Crime Analytics with MapReduce

SE446 Big Data Engineering — Group Project MapReduce pipeline built on a Hadoop cluster to analyze Chicago crime data (8M+ records). Tasks include crime type distribution, location hotspots, yearly crime trends, and arrest analysis using Python-based MapReduce Streaming.

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

## Task Assignments

| Task   | Description              | Assigned To             |
|--------|--------------------------|-------------------------|
| Task 1 | GitHub Setup & PR Review | Ahmad Fares Mzayek      |
| Task 2 | Crime Type Distribution  | Faisal Hajj Khalil      |
| Task 3 | Location Hotspots        | Tanzim Alam             |
| Task 4 | Year Trend Analysis      | Mohammad Ghassan Hussen |
| Task 5 | Arrest Analysis          | Bilal Othman            |

---

## Executive Summary

This project implements a MapReduce pipeline on a Hadoop cluster to analyze the Chicago Crime dataset (8M+ records spanning 2001–2025). Each task is implemented as a Python mapper paired with a generic sum reducer, executed using Hadoop Streaming. The pipeline answers four key questions for the Chicago Police Department: which crime types are most prevalent, which locations are highest risk, how crime volume has changed over the years, and what percentage of crimes result in an arrest.

---

## Results

### Task 2: Crime Type Distribution
**Research Question:** What are the most common types of crimes in Chicago?

**MapReduce Command:**
```bash
mapred streaming \
  -files src/mapper_task2.py,src/reducer_sum.py \
  -mapper "python3 mapper_task2.py" \
  -reducer "python3 reducer_sum.py" \
  -input /data/chicago_crimes.csv \
  -output /user/fhajjkhalil/project/m1/task2
```

**Top 5 Results:**

*(To be filled in once Faisal submits)*

**Interpretation:** *(To be filled in once Faisal submits)*

**Execution Log:**

*(To be filled in once Faisal submits)*

---

### Task 3: Location Hotspots
**Research Question:** Where do most crimes occur?

**MapReduce Command:**
```bash
mapred streaming \
  -files src/mapper_task3.py,src/reducer_sum.py \
  -mapper "python3 mapper_task3.py" \
  -reducer "python3 reducer_sum.py" \
  -input /data/chicago_crimes.csv \
  -output /user/talam/project/m1/task3
```

**Top 5 Results:**

*(To be filled in once Tanzim submits)*

**Interpretation:** *(To be filled in once Tanzim submits)*

**Execution Log:**

*(To be filled in once Tanzim submits)*

---

### Task 4: Year Trend Analysis
**Research Question:** How has the total number of crimes changed over the years?

**MapReduce Command:**
```bash
mapred streaming \
  -files mapper_task4.py,reducer_sum.py \
  -mapper "python3 mapper_task4.py" \
  -reducer "python3 reducer_sum.py" \
  -input /data/chicago_crimes.csv \
  -output /user/mhussen/project/m1/task4
```

**Top 5 Results (Highest Crime Years):**

| Year | Crime Count |
|------|-------------|
| 2001 | 467,301     |
| 2002 | 205,267     |
| 2023 | 81,461      |
| 2025 | 12,710      |
| 2022 | 4,678       |

**Interpretation:** Crime volume was highest in 2001 (467,301 incidents) and has generally declined over the years, with a notable spike in 2023 (81,461 incidents). The lower counts in recent years (2024–2025) likely reflect incomplete data for those years rather than a true drop in crime.

**Execution Log:**

<details>
<summary>Click to expand full execution log</summary>
```
mhussen@master-node:~$ source /etc/profile.d/hadoop.sh
mhussen@master-node:~$ mapred streaming \
 -files mapper_task4.py,reducer_sum.py \
 -mapper "python3 mapper_task4.py" \
 -reducer "python3 reducer_sum.py" \
 -input /data/chicago_crimes_sample.csv \
 -output /user/mhussen/project/m1/task4_sample
packageJobJar: [] [/opt/hadoop-3.4.1/share/hadoop/tools/lib/hadoop-streaming-3.4.1.jar] /tmp/streamjob16166768054372296438.jar tmpDir=null
2026-03-23 17:07:23,196 INFO client.DefaultNoHARMFailoverProxyProvider: Connecting to ResourceManager at master-node/134.209.172.50:8032
2026-03-23 17:07:23,539 INFO client.DefaultNoHARMFailoverProxyProvider: Connecting to ResourceManager at master-node/134.209.172.50:8032
2026-03-23 17:07:24,076 INFO mapreduce.JobResourceUploader: Disabling Erasure Coding for path: /tmp/hadoop-yarn/staging/mhussen/.staging/job_1771402826595_0126
2026-03-23 17:07:25,910 INFO mapred.FileInputFormat: Total input files to process : 1
2026-03-23 17:07:26,591 INFO mapreduce.JobSubmitter: number of splits:2
2026-03-23 17:07:27,503 INFO mapreduce.JobSubmitter: Submitting tokens for job: job_1771402826595_0126
2026-03-23 17:07:27,503 INFO mapreduce.JobSubmitter: Executing with tokens: []
2026-03-23 17:07:27,844 INFO conf.Configuration: resource-types.xml not found
2026-03-23 17:07:27,844 INFO resource.ResourceUtils: Unable to find 'resource-types.xml'.
2026-03-23 17:07:27,981 INFO impl.YarnClientImpl: Submitted application application_1771402826595_0126
2026-03-23 17:07:28,047 INFO mapreduce.Job: The url to track the job: http://master-node:8088/proxy/application_1771402826595_0126/
2026-03-23 17:07:28,051 INFO mapreduce.Job: Running job: job_1771402826595_0126
2026-03-23 17:07:44,832 INFO mapreduce.Job: Job job_1771402826595_0126 running in uber mode : false
2026-03-23 17:07:44,837 INFO mapreduce.Job:  map 0% reduce 0%
2026-03-23 17:08:03,682 INFO mapreduce.Job:  map 50% reduce 0%
2026-03-23 17:08:04,875 INFO mapreduce.Job:  map 100% reduce 0%
2026-03-23 17:08:15,596 INFO mapreduce.Job:  map 100% reduce 100%
2026-03-23 17:08:18,349 INFO mapreduce.Job: Job job_1771402826595_0126 completed successfully
2026-03-23 17:08:18,583 INFO mapreduce.Job: Counters: 54
        File System Counters
                FILE: Number of bytes read=90006
                FILE: Number of bytes written=1123148
                FILE: Number of read operations=0
                FILE: Number of large read operations=0
                FILE: Number of write operations=0
                HDFS: Number of bytes read=2391502
                HDFS: Number of bytes written=185
                HDFS: Number of read operations=11
                HDFS: Number of large read operations=0
                HDFS: Number of write operations=2
                HDFS: Number of bytes read erasure-coded=0
        Job Counters
                Launched map tasks=2
                Launched reduce tasks=1
                Data-local map tasks=2
                Total time spent by all maps in occupied slots (ms)=65624
                Total time spent by all reduces in occupied slots (ms)=19962
                Total time spent by all map tasks (ms)=32812
                Total time spent by all reduce tasks (ms)=9981
                Total vcore-milliseconds taken by all map tasks=32812
                Total vcore-milliseconds taken by all reduce tasks=9981
                Total megabyte-milliseconds taken by all map tasks=16799744
                Total megabyte-milliseconds taken by all reduce tasks=5110272
        Map-Reduce Framework
                Map input records=10001
                Map output records=10000
                Map output bytes=70000
                Map output materialized bytes=90012
                Input split bytes=212
                Combine input records=0
                Combine output records=0
                Reduce input groups=24
                Reduce shuffle bytes=90012
                Reduce input records=10000
                Reduce output records=24
                Spilled Records=20000
                Shuffled Maps =2
                Failed Shuffles=0
                Merged Map outputs=2
                GC time elapsed (ms)=776
                CPU time spent (ms)=4190
                Physical memory (bytes) snapshot=675246080
                Virtual memory (bytes) snapshot=6562586624
                Total committed heap usage (bytes)=348151808
                Peak Map Physical memory (bytes)=263626752
                Peak Map Virtual memory (bytes)=2187796480
                Peak Reduce Physical memory (bytes)=150110208
                Peak Reduce Virtual memory (bytes)=2189676544
        Shuffle Errors
                BAD_ID=0
                CONNECTION=0
                IO_ERROR=0
                WRONG_LENGTH=0
                WRONG_MAP=0
                WRONG_REDUCE=0
        File Input Format Counters
                Bytes Read=2391290
        File Output Format Counters
                Bytes Written=185
2026-03-23 17:08:18,589 INFO streaming.StreamJob: Output directory: /user/mhussen/project/m1/task4_sample
mhussen@master-node:~$ hdfs dfs -cat /user/mhussen/project/m1/task4_sample/part-*
2001    4
2002    2
2003    1
2004    6
2005    19
2006    4
2007    7
2008    16
2009    5
2010    5
2011    7
2012    9
2013    10
2014    16
2015    28
2016    20
2017    49
2018    28
2019    36
2020    25
2021    83
2022    135
2023    9446
2024    39
mhussen@master-node:~$ mapred streaming \
 -files mapper_task4.py,reducer_sum.py \
 -mapper "python3 mapper_task4.py" \
 -reducer "python3 reducer_sum.py" \
 -input /data/chicago_crimes.csv \
 -output /user/mhussen/project/m1/task4
packageJobJar: [] [/opt/hadoop-3.4.1/share/hadoop/tools/lib/hadoop-streaming-3.4.1.jar] /tmp/streamjob10935975483283575454.jar tmpDir=null
2026-03-23 17:10:38,274 INFO client.DefaultNoHARMFailoverProxyProvider: Connecting to ResourceManager at master-node/134.209.172.50:8032
2026-03-23 17:10:38,530 INFO client.DefaultNoHARMFailoverProxyProvider: Connecting to ResourceManager at master-node/134.209.172.50:8032
2026-03-23 17:10:39,014 INFO mapreduce.JobResourceUploader: Disabling Erasure Coding for path: /tmp/hadoop-yarn/staging/mhussen/.staging/job_1771402826595_0127
2026-03-23 17:10:40,692 INFO mapred.FileInputFormat: Total input files to process : 1
2026-03-23 17:10:40,727 INFO net.NetworkTopology: Adding a new node: /default-rack/164.92.103.148:9866
2026-03-23 17:10:40,728 INFO net.NetworkTopology: Adding a new node: /default-rack/146.190.147.119:9866
2026-03-23 17:10:41,349 INFO mapreduce.JobSubmitter: number of splits:2
2026-03-23 17:10:42,098 INFO mapreduce.JobSubmitter: Submitting tokens for job: job_1771402826595_0127
2026-03-23 17:10:42,098 INFO mapreduce.JobSubmitter: Executing with tokens: []
2026-03-23 17:10:42,458 INFO conf.Configuration: resource-types.xml not found
2026-03-23 17:10:42,458 INFO resource.ResourceUtils: Unable to find 'resource-types.xml'.
2026-03-23 17:10:42,565 INFO impl.YarnClientImpl: Submitted application application_1771402826595_0127
2026-03-23 17:10:42,612 INFO mapreduce.Job: The url to track the job: http://master-node:8088/proxy/application_1771402826595_0127/
2026-03-23 17:10:42,614 INFO mapreduce.Job: Running job: job_1771402826595_0127
2026-03-23 17:11:01,477 INFO mapreduce.Job: Job job_1771402826595_0127 running in uber mode : false
2026-03-23 17:11:01,479 INFO mapreduce.Job:  map 0% reduce 0%
2026-03-23 17:11:27,574 INFO mapreduce.Job:  map 100% reduce 0%
2026-03-23 17:11:43,393 INFO mapreduce.Job:  map 100% reduce 100%
2026-03-23 17:11:46,243 INFO mapreduce.Job: Job job_1771402826595_0127 completed successfully
2026-03-23 17:11:46,479 INFO mapreduce.Job: Counters: 54
        File System Counters
                FILE: Number of bytes read=7137663
                FILE: Number of bytes written=15218420
                FILE: Number of read operations=0
                FILE: Number of large read operations=0
                FILE: Number of write operations=0
                HDFS: Number of bytes read=181964998
                HDFS: Number of bytes written=245
                HDFS: Number of read operations=11
                HDFS: Number of large read operations=0
                HDFS: Number of write operations=2
                HDFS: Number of bytes read erasure-coded=0
        Job Counters
                Launched map tasks=2
                Launched reduce tasks=1
                Data-local map tasks=2
                Total time spent by all maps in occupied slots (ms)=94514
                Total time spent by all reduces in occupied slots (ms)=27010
                Total time spent by all map tasks (ms)=47257
                Total time spent by all reduce tasks (ms)=13505
                Total vcore-milliseconds taken by all map tasks=47257
                Total vcore-milliseconds taken by all reduce tasks=13505
                Total megabyte-milliseconds taken by all map tasks=24195584
                Total megabyte-milliseconds taken by all reduce tasks=6914560
        Map-Reduce Framework
                Map input records=793074
                Map output records=793073
                Map output bytes=5551511
                Map output materialized bytes=7137669
                Input split bytes=198
                Combine input records=0
                Combine output records=0
                Reduce input groups=25
                Reduce shuffle bytes=7137669
                Reduce input records=793073
                Reduce output records=25
                Spilled Records=1586146
                Shuffled Maps =2
                Failed Shuffles=0
                Merged Map outputs=2
                GC time elapsed (ms)=769
                CPU time spent (ms)=11710
                Physical memory (bytes) snapshot=701296640
                Virtual memory (bytes) snapshot=6568706048
                Total committed heap usage (bytes)=348102656
                Peak Map Physical memory (bytes)=276606976
                Peak Map Virtual memory (bytes)=2189856768
                Peak Reduce Physical memory (bytes)=157880320
                Peak Reduce Virtual memory (bytes)=2193289216
        Shuffle Errors
                BAD_ID=0
                CONNECTION=0
                IO_ERROR=0
                WRONG_LENGTH=0
                WRONG_MAP=0
                WRONG_REDUCE=0
        File Input Format Counters
                Bytes Read=181964800
        File Output Format Counters
                Bytes Written=245
2026-03-23 17:11:46,479 INFO streaming.StreamJob: Output directory: /user/mhussen/project/m1/task4
mhussen@master-node:~$ hdfs dfs -cat /user/mhussen/project/m1/task4/part-*
2001    467301
2002    205267
2003    985
2004    915
2005    1031
2006    796
2007    762
2008    1010
2009    910
2010    695
2011    770
2012    800
2013    714
2014    825
2015    1105
2016    1339
2017    1387
2018    1327
2019    1174
2020    1832
2021    2399
2022    4678
2023    81461
2024    880
2025    12710
mhussen@master-node:~$
```

</details>

---

### Task 5: Arrest Analysis
**Research Question:** What percentage of crimes result in an arrest?

**MapReduce Command:**
```bash
mapred streaming \
  -files src/mapper_task5.py,src/reducer_sum.py \
  -mapper "python3 mapper_task5.py" \
  -reducer "python3 reducer_sum.py" \
  -input /data/chicago_crimes.csv \
  -output /user/bothman/project/m1/task5
```

**Results:**

*(To be filled in once Bilal submits)*

**Interpretation:** *(To be filled in once Bilal submits)*

**Execution Log:**

*(To be filled in once Bilal submits)*

---

## Member Contributions

| Name                    | Contribution                                                    |
|-------------------------|-----------------------------------------------------------------|
| Ahmad Fares Mzayek      | GitHub repository setup, branch management, PR review and merge |
| Faisal Hajj Khalil      | Wrote mapper_task2.py, ran Task 2 on cluster, committed results |
| Tanzim Alam             | Wrote mapper_task3.py, ran Task 3 on cluster, committed results |
| Mohammad Ghassan Hussen | Wrote mapper_task4.py, ran Task 4 on cluster, committed results |
| Bilal Othman            | Wrote mapper_task5.py, ran Task 5 on cluster, committed results |

---

*SE446 Big Data Engineering — Group Project*  
