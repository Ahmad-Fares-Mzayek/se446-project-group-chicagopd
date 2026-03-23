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
                HDFS: Number of bytes read=2391502
                HDFS: Number of bytes written=185
        Job Counters
                Launched map tasks=2
                Launched reduce tasks=1
                Data-local map tasks=2
        Map-Reduce Framework
                Map input records=10001
                Map output records=10000
                Reduce input groups=24
                Reduce output records=24
        File Input Format Counters
                Bytes Read=2391290
        File Output Format Counters
                Bytes Written=185
2026-03-23 17:08:18,589 INFO streaming.StreamJob: Output directory: /user/mhussen/project/m1/task4_sample

Sample Results:
2001    4
2002    2
2003    1
...
2023    9446
2024    39

mhussen@master-node:~$ mapred streaming \
 -files mapper_task4.py,reducer_sum.py \
 -mapper "python3 mapper_task4.py" \
 -reducer "python3 reducer_sum.py" \
 -input /data/chicago_crimes.csv \
 -output /user/mhussen/project/m1/task4
...
2026-03-23 17:11:46,243 INFO mapreduce.Job: Job job_1771402826595_0127 completed successfully
        Map-Reduce Framework
                Map input records=793074
                Map output records=793073
                Reduce input groups=25
                Reduce output records=25
2026-03-23 17:11:46,479 INFO streaming.StreamJob: Output directory: /user/mhussen/project/m1/task4

Full Results:
2001    467301
2002    205267
2003    985
...
2024    880
2025    12710
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

| Name                    | Contribution                                              |
|-------------------------|-----------------------------------------------------------|
| Ahmad Fares Mzayek      | GitHub repository setup, branch management, PR review and merge |
| Faisal Hajj Khalil      | Wrote mapper_task2.py, ran Task 2 on cluster, committed results |
| Tanzim Alam             | Wrote mapper_task3.py, ran Task 3 on cluster, committed results |
| Mohammad Ghassan Hussen | Wrote mapper_task4.py, ran Task 4 on cluster, committed results |
| Bilal Othman            | Wrote mapper_task5.py, ran Task 5 on cluster, committed results |

---

*SE446 Big Data Engineering — Group Project*
