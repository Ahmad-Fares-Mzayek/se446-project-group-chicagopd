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

This project implements a MapReduce pipeline on a Hadoop cluster to analyze the Chicago Crime dataset spanning 2001–2025, containing over 793,000 records. The goal was to provide the Chicago Police Department with actionable intelligence on crime patterns.

Each task follows the same MapReduce architecture: a Python mapper reads CSV lines from standard input, extracts the relevant field at a specific column index, and emits key-value pairs. A shared generic sum reducer then aggregates counts per key. All jobs were executed using Hadoop Streaming on a 3-node Hadoop 3.4.1 cluster (1 master, 2 workers), first validated on a 10,000-record sample dataset before being run on the full dataset.

Key findings: Theft is the most prevalent crime type (162,688 incidents), Street is the most common crime location (245,437 incidents), crime volume peaked in 2001 and has generally declined since, and only 27.1% of crimes result in an arrest.

---

## Implementation

### Architecture

All four analytical tasks share the same MapReduce pattern:
```
CSV line (from HDFS)
      ↓
  Mapper (Python)
  - Parse CSV line by splitting on commas
  - Skip header row (parts[0] == 'ID')
  - Extract target field by column index
  - Emit: print(f"{key}\t1")
      ↓
  Hadoop Shuffle & Sort
  - Groups all values by key
  - Sorts keys alphabetically
      ↓
  Reducer (Python) — same file for all tasks
  - Reads sorted key-value pairs
  - Accumulates count per key
  - Emits: print(f"{key}\t{total}")
      ↓
  Output stored in HDFS
```

### Dataset

| Property | Value |
|----------|-------|
| Full dataset path | `/data/chicago_crimes.csv` |
| Sample dataset path | `/data/chicago_crimes_sample.csv` |
| Full dataset records | 793,073 |
| Sample records | 10,000 |
| Format | CSV with header row |

### Column Index Reference

| Index | Field | Used In |
|-------|-------|---------|
| 2 | Date | Task 4 |
| 5 | Primary Type | Task 2 |
| 7 | Location Description | Task 3 |
| 8 | Arrest | Task 5 |

### Shared Reducer (`reducer_sum.py`)

The same reducer was used for all four tasks without modification. It reads tab-separated key-value pairs from standard input, accumulates counts per key, and emits the final totals:
```python
#!/usr/bin/env python3
import sys

current_key = None
current_total = 0

for line in sys.stdin:
    line = line.strip()
    try:
        key, count = line.split('\t', 1)
        count = int(count)
    except ValueError:
        continue
    if current_key == key:
        current_total += count
    else:
        if current_key:
            print(f"{current_key}\t{current_total}")
        current_key = key
        current_total = count

if current_key:
    print(f"{current_key}\t{current_total}")
```

---

## Results

### Task 2: Crime Type Distribution
**Research Question:** What are the most common types of crimes in Chicago?

**Mapper logic:** Extract `parts[5]` (Primary Type), skip header, emit `(crime_type, 1)` for every record.

**MapReduce Command (Sample):**
```bash
mapred streaming \
  -files mapper_task2.py,reducer_sum.py \
  -mapper "python3 mapper_task2.py" \
  -reducer "python3 reducer_sum.py" \
  -input /data/chicago_crimes_sample.csv \
  -output /user/fkhalil/project/m1/task2_sample
```

**MapReduce Command (Full Dataset):**
```bash
mapred streaming \
  -files mapper_task2.py,reducer_sum.py \
  -mapper "python3 mapper_task2.py" \
  -reducer "python3 reducer_sum.py" \
  -input /data/chicago_crimes.csv \
  -output /user/fkhalil/project/m1/task2
```

**Top 5 Results:**

| Rank | Crime Type | Count |
|------|------------|-------|
| 1 | THEFT | 162,688 |
| 2 | BATTERY | 151,930 |
| 3 | CRIMINAL DAMAGE | 91,241 |
| 4 | NARCOTICS | 74,127 |
| 5 | ASSAULT | 54,070 |

**Interpretation:** Theft is the most prevalent crime in Chicago with 162,688 incidents, followed closely by Battery at 151,930. These two categories alone account for a significant portion of all reported crimes, suggesting that property crime and physical altercations are the primary concerns for law enforcement resource allocation.

**Execution Log:**

<details>
<summary>Click to expand full execution log</summary>
```
fkhalil@master-node:~$ source /etc/profile.d/hadoop.sh
fkhalil@master-node:~$ mapred streaming \
-files mapper_task2.py,reducer_sum.py \
-mapper "python3 mapper_task2.py" \
-reducer "python3 reducer_sum.py" \
-input /data/chicago_crimes_sample.csv \
-output /user/fkhalil/project/m1/task2_sample
packageJobJar: [] [/opt/hadoop-3.4.1/share/hadoop/tools/lib/hadoop-streaming-3.4.1.jar] /tmp/streamjob7682691905380599919.jar tmpDir=null
2026-03-24 12:14:04,540 INFO client.DefaultNoHARMFailoverProxyProvider: Connecting to ResourceManager at master-node/134.209.172.50:8032
2026-03-24 12:14:04,816 INFO client.DefaultNoHARMFailoverProxyProvider: Connecting to ResourceManager at master-node/134.209.172.50:8032
2026-03-24 12:14:05,217 INFO mapreduce.JobResourceUploader: Disabling Erasure Coding for path: /tmp/hadoop-yarn/staging/fkhalil/.staging/job_1771402826595_0158
2026-03-24 12:14:06,863 INFO mapred.FileInputFormat: Total input files to process : 1
2026-03-24 12:14:07,575 INFO mapreduce.JobSubmitter: number of splits:2
2026-03-24 12:14:08,345 INFO mapreduce.JobSubmitter: Submitting tokens for job: job_1771402826595_0158
2026-03-24 12:14:08,345 INFO mapreduce.JobSubmitter: Executing with tokens: []
2026-03-24 12:14:08,602 INFO conf.Configuration: resource-types.xml not found
2026-03-24 12:14:08,603 INFO resource.ResourceUtils: Unable to find 'resource-types.xml'.
2026-03-24 12:14:08,688 INFO impl.YarnClientImpl: Submitted application application_1771402826595_0158
2026-03-24 12:14:08,726 INFO mapreduce.Job: The url to track the job: http://master-node:8088/proxy/application_1771402826595_0158/
2026-03-24 12:14:08,727 INFO mapreduce.Job: Running job: job_1771402826595_0158
2026-03-24 12:14:26,506 INFO mapreduce.Job: Job job_1771402826595_0158 running in uber mode : false
2026-03-24 12:14:26,508 INFO mapreduce.Job:  map 0% reduce 0%
2026-03-24 12:14:46,240 INFO mapreduce.Job:  map 100% reduce 0%
2026-03-24 12:14:55,986 INFO mapreduce.Job:  map 100% reduce 100%
2026-03-24 12:14:58,849 INFO mapreduce.Job: Job job_1771402826595_0158 completed successfully
2026-03-24 12:14:59,058 INFO mapreduce.Job: Counters: 54
	File System Counters
		FILE: Number of bytes read=159339
		FILE: Number of bytes written=1261811
		FILE: Number of read operations=0
		FILE: Number of large read operations=0
		FILE: Number of write operations=0
		HDFS: Number of bytes read=2391502
		HDFS: Number of bytes written=541
		HDFS: Number of read operations=11
		HDFS: Number of large read operations=0
		HDFS: Number of write operations=2
		HDFS: Number of bytes read erasure-coded=0
	Job Counters
		Launched map tasks=2
		Launched reduce tasks=1
		Data-local map tasks=2
		Total time spent by all maps in occupied slots (ms)=64954
		Total time spent by all reduces in occupied slots (ms)=15882
		Total time spent by all map tasks (ms)=32477
		Total time spent by all reduce tasks (ms)=7941
		Total vcore-milliseconds taken by all map tasks=32477
		Total vcore-milliseconds taken by all reduce tasks=7941
		Total megabyte-milliseconds taken by all map tasks=16628224
		Total megabyte-milliseconds taken by all reduce tasks=4065792
	Map-Reduce Framework
		Map input records=10001
		Map output records=10000
		Map output bytes=139333
		Map output materialized bytes=159345
		Input split bytes=212
		Combine input records=0
		Combine output records=0
		Reduce input groups=29
		Reduce shuffle bytes=159345
		Reduce input records=10000
		Reduce output records=29
		Spilled Records=20000
		Shuffled Maps =2
		Failed Shuffles=0
		Merged Map outputs=2
		GC time elapsed (ms)=591
		CPU time spent (ms)=3310
		Physical memory (bytes) snapshot=649420800
		Virtual memory (bytes) snapshot=6566498304
		Total committed heap usage (bytes)=348164096
		Peak Map Physical memory (bytes)=255819776
		Peak Map Virtual memory (bytes)=2188947456
		Peak Reduce Physical memory (bytes)=146571264
		Peak Reduce Virtual memory (bytes)=2191974400
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
		Bytes Written=541
2026-03-24 12:14:59,062 INFO streaming.StreamJob: Output directory: /user/fkhalil/project/m1/task2_sample
fkhalil@master-node:~$ hdfs dfs -cat /user/fkhalil/project/m1/task2_sample/part-*
ARSON	21
ASSAULT	878
BATTERY	1728
BURGLARY	316
CONCEALED CARRY LICENSE VIOLATION	6
CRIM SEXUAL ASSAULT	4
CRIMINAL DAMAGE	1062
CRIMINAL SEXUAL ASSAULT	107
CRIMINAL TRESPASS	153
DECEPTIVE PRACTICE	799
GAMBLING	1
HOMICIDE	44
HUMAN TRAFFICKING	2
INTERFERENCE WITH PUBLIC OFFICER	26
INTIMIDATION	5
KIDNAPPING	5
LIQUOR LAW VIOLATION	6
MOTOR VEHICLE THEFT	948
NARCOTICS	159
OBSCENITY	1
OFFENSE INVOLVING CHILDREN	137
OTHER OFFENSE	586
PROSTITUTION	6
PUBLIC PEACE VIOLATION	34
ROBBERY	508
SEX OFFENSE	96
STALKING	24
THEFT	2054
WEAPONS VIOLATION	284
fkhalil@master-node:~$ mapred streaming \
-files mapper_task2.py,reducer_sum.py \
-mapper "python3 mapper_task2.py" \
-reducer "python3 reducer_sum.py" \
-input /data/chicago_crimes.csv \
-output /user/fkhalil/project/m1/task2
packageJobJar: [] [/opt/hadoop-3.4.1/share/hadoop/tools/lib/hadoop-streaming-3.4.1.jar] /tmp/streamjob1014381503671355865.jar tmpDir=null
2026-03-24 12:15:44,277 INFO client.DefaultNoHARMFailoverProxyProvider: Connecting to ResourceManager at master-node/134.209.172.50:8032
2026-03-24 12:15:44,558 INFO client.DefaultNoHARMFailoverProxyProvider: Connecting to ResourceManager at master-node/134.209.172.50:8032
2026-03-24 12:15:45,033 INFO mapreduce.JobResourceUploader: Disabling Erasure Coding for path: /tmp/hadoop-yarn/staging/fkhalil/.staging/job_1771402826595_0159
2026-03-24 12:15:46,802 INFO mapred.FileInputFormat: Total input files to process : 1
2026-03-24 12:15:46,824 INFO net.NetworkTopology: Adding a new node: /default-rack/146.190.147.119:9866
2026-03-24 12:15:46,825 INFO net.NetworkTopology: Adding a new node: /default-rack/164.92.103.148:9866
2026-03-24 12:15:47,454 INFO mapreduce.JobSubmitter: number of splits:2
2026-03-24 12:15:48,305 INFO mapreduce.JobSubmitter: Submitting tokens for job: job_1771402826595_0159
2026-03-24 12:15:48,306 INFO mapreduce.JobSubmitter: Executing with tokens: []
2026-03-24 12:15:48,693 INFO conf.Configuration: resource-types.xml not found
2026-03-24 12:15:48,693 INFO resource.ResourceUtils: Unable to find 'resource-types.xml'.
2026-03-24 12:15:48,788 INFO impl.YarnClientImpl: Submitted application application_1771402826595_0159
2026-03-24 12:15:48,848 INFO mapreduce.Job: The url to track the job: http://master-node:8088/proxy/application_1771402826595_0159/
2026-03-24 12:15:48,851 INFO mapreduce.Job: Running job: job_1771402826595_0159
2026-03-24 12:16:06,627 INFO mapreduce.Job: Job job_1771402826595_0159 running in uber mode : false
2026-03-24 12:16:06,629 INFO mapreduce.Job:  map 0% reduce 0%
2026-03-24 12:16:32,901 INFO mapreduce.Job:  map 100% reduce 0%
2026-03-24 12:16:47,742 INFO mapreduce.Job:  map 100% reduce 100%
2026-03-24 12:16:50,700 INFO mapreduce.Job: Job job_1771402826595_0159 completed successfully
2026-03-24 12:16:50,979 INFO mapreduce.Job: Counters: 54
	File System Counters
		FILE: Number of bytes read=11798790
		FILE: Number of bytes written=24540671
		FILE: Number of read operations=0
		FILE: Number of large read operations=0
		FILE: Number of write operations=0
		HDFS: Number of bytes read=181964998
		HDFS: Number of bytes written=690
		HDFS: Number of read operations=11
		HDFS: Number of large read operations=0
		HDFS: Number of write operations=2
		HDFS: Number of bytes read erasure-coded=0
	Job Counters
		Launched map tasks=2
		Launched reduce tasks=1
		Data-local map tasks=2
		Total time spent by all maps in occupied slots (ms)=92670
		Total time spent by all reduces in occupied slots (ms)=24264
		Total time spent by all map tasks (ms)=46335
		Total time spent by all reduce tasks (ms)=12132
		Total vcore-milliseconds taken by all map tasks=46335
		Total vcore-milliseconds taken by all reduce tasks=12132
		Total megabyte-milliseconds taken by all map tasks=23723520
		Total megabyte-milliseconds taken by all reduce tasks=6211584
	Map-Reduce Framework
		Map input records=793074
		Map output records=793072
		Map output bytes=10212640
		Map output materialized bytes=11798796
		Input split bytes=198
		Combine input records=0
		Combine output records=0
		Reduce input groups=34
		Reduce shuffle bytes=11798796
		Reduce input records=793072
		Reduce output records=34
		Spilled Records=1586144
		Shuffled Maps =2
		Failed Shuffles=0
		Merged Map outputs=2
		GC time elapsed (ms)=702
		CPU time spent (ms)=9840
		Physical memory (bytes) snapshot=685572096
		Virtual memory (bytes) snapshot=6565597184
		Total committed heap usage (bytes)=348209152
		Peak Map Physical memory (bytes)=256753664
		Peak Map Virtual memory (bytes)=2189635584
		Peak Reduce Physical memory (bytes)=177852416
		Peak Reduce Virtual memory (bytes)=2190397440
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
		Bytes Written=690
2026-03-24 12:16:50,984 INFO streaming.StreamJob: Output directory: /user/fkhalil/project/m1/task2
fkhalil@master-node:~$ hdfs dfs -cat /user/fkhalil/project/m1/task2/part-*
ARSON	1717
ASSAULT	54070
BATTERY	151930
BURGLARY	39872
CONCEALED CARRY LICENSE VIOLATION	77
CRIM SEXUAL ASSAULT	2463
CRIMINAL DAMAGE	91241
CRIMINAL SEXUAL ASSAULT	1372
CRIMINAL TRESPASS	21476
DECEPTIVE PRACTICE	30396
DOMESTIC VIOLENCE	1
GAMBLING	1314
HOMICIDE	13173
HUMAN TRAFFICKING	13
INTERFERENCE WITH PUBLIC OFFICER	803
INTIMIDATION	92
KIDNAPPING	1108
LIQUOR LAW VIOLATION	2349
MOTOR VEHICLE THEFT	48494
NARCOTICS	74127
NON-CRIMINAL	1
OBSCENITY	24
OFFENSE INVOLVING CHILDREN	2065
OTHER NARCOTIC VIOLATION	11
OTHER OFFENSE	36893
PROSTITUTION	9100
PUBLIC INDECENCY	17
PUBLIC PEACE VIOLATION	1827
RITUALISM	8
ROBBERY	30991
SEX OFFENSE	3932
STALKING	534
THEFT	162688
WEAPONS VIOLATION	8893
fkhalil@master-node:~$
```

</details>

---

### Task 3: Location Hotspots
**Research Question:** Where do most crimes occur?

**Mapper logic:** Extract `parts[7]` (Location Description), skip header, emit `(location, 1)` for every record.

**MapReduce Command (Sample):**
```bash
mapred streaming \
  -files mapper_task3.py,reducer_sum.py \
  -mapper "python3 mapper_task3.py" \
  -reducer "python3 reducer_sum.py" \
  -input /data/chicago_crimes_sample.csv \
  -output /user/tanalam/project/m1/task3_sample
```

**MapReduce Command (Full Dataset):**
```bash
mapred streaming \
  -files mapper_task3.py,reducer_sum.py \
  -mapper "python3 mapper_task3.py" \
  -reducer "python3 reducer_sum.py" \
  -input /data/chicago_crimes.csv \
  -output /user/tanalam/project/m1/task3
```

**Top 5 Results:**

| Rank | Location | Count |
|------|----------|-------|
| 1 | STREET | 245,437 |
| 2 | RESIDENCE | 136,238 |
| 3 | APARTMENT | 60,925 |
| 4 | SIDEWALK | 47,407 |
| 5 | OTHER | 29,213 |

**Interpretation:** Streets are by far the most common crime location with 245,437 incidents, nearly double the next highest location (Residence at 136,238). Combined with Sidewalk (47,407), outdoor public spaces account for the majority of crime locations, indicating that patrol units should prioritize street-level presence.

**Execution Log:**

<details>
<summary>Click to expand full execution log</summary>
```
tanalam@master-node:~$ mapred streaming -files mapper_task3.py,reducer_sum.py -mapper "python3 mapper_task3.py" -reducer "python3 reducer_sum.py" -input /data/chicago_crimes_sample.csv -output /user/tanalam/project/m1/task3_sample
packageJobJar: [] [/opt/hadoop-3.4.1/share/hadoop/tools/lib/hadoop-streaming-3.4.1.jar] /tmp/streamjob18250072783356417397.jar tmpDir=null
2026-03-25 23:24:33,365 INFO client.DefaultNoHARMFailoverProxyProvider: Connecting to ResourceManager at master-node/134.209.172.50:8032
2026-03-25 23:24:33,655 INFO client.DefaultNoHARMFailoverProxyProvider: Connecting to ResourceManager at master-node/134.209.172.50:8032
2026-03-25 23:24:34,097 INFO mapreduce.JobResourceUploader: Disabling Erasure Coding for path: /tmp/hadoop-yarn/staging/tanalam/.staging/job_1771402826595_0221
2026-03-25 23:24:35,821 INFO mapred.FileInputFormat: Total input files to process : 1
2026-03-25 23:24:36,482 INFO mapreduce.JobSubmitter: number of splits:2
2026-03-25 23:24:37,438 INFO mapreduce.JobSubmitter: Submitting tokens for job: job_1771402826595_0221
2026-03-25 23:24:37,438 INFO mapreduce.JobSubmitter: Executing with tokens: []
2026-03-25 23:24:37,726 INFO conf.Configuration: resource-types.xml not found
2026-03-25 23:24:37,726 INFO resource.ResourceUtils: Unable to find 'resource-types.xml'.
2026-03-25 23:24:37,838 INFO impl.YarnClientImpl: Submitted application application_1771402826595_0221
2026-03-25 23:24:37,882 INFO mapreduce.Job: The url to track the job: http://master-node:8088/proxy/application_1771402826595_0221/
2026-03-25 23:24:37,884 INFO mapreduce.Job: Running job: job_1771402826595_0221
2026-03-25 23:24:53,623 INFO mapreduce.Job: Job job_1771402826595_0221 running in uber mode : false
2026-03-25 23:24:53,625 INFO mapreduce.Job:  map 0% reduce 0%
2026-03-25 23:25:15,624 INFO mapreduce.Job:  map 100% reduce 0%
2026-03-25 23:25:26,573 INFO mapreduce.Job:  map 100% reduce 100%
2026-03-25 23:25:29,430 INFO mapreduce.Job: Job job_1771402826595_0221 completed successfully
2026-03-25 23:25:29,687 INFO mapreduce.Job: Counters: 54
        File System Counters
                FILE: Number of bytes read=166017
                FILE: Number of bytes written=1275170
                FILE: Number of read operations=0
                FILE: Number of large read operations=0
                FILE: Number of write operations=0
                HDFS: Number of bytes read=2391502
                HDFS: Number of bytes written=2673
                HDFS: Number of read operations=11
                HDFS: Number of large read operations=0
                HDFS: Number of write operations=2
                HDFS: Number of bytes read erasure-coded=0
        Job Counters
                Launched map tasks=2
                Launched reduce tasks=1
                Data-local map tasks=2
                Total time spent by all maps in occupied slots (ms)=74748
                Total time spent by all reduces in occupied slots (ms)=15546
                Total time spent by all map tasks (ms)=37374
                Total time spent by all reduce tasks (ms)=7773
                Total vcore-milliseconds taken by all map tasks=37374
                Total vcore-milliseconds taken by all reduce tasks=7773
                Total megabyte-milliseconds taken by all map tasks=19135488
                Total megabyte-milliseconds taken by all reduce tasks=3979776
        Map-Reduce Framework
                Map input records=10001
                Map output records=10000
                Map output bytes=146011
                Map output materialized bytes=166023
                Input split bytes=212
                Combine input records=0
                Combine output records=0
                Reduce input groups=116
                Reduce shuffle bytes=166023
                Reduce input records=10000
                Reduce output records=115
                Spilled Records=20000
                Shuffled Maps =2
                Failed Shuffles=0
                Merged Map outputs=2
                GC time elapsed (ms)=614
                CPU time spent (ms)=3240
                Physical memory (bytes) snapshot=645414912
                Virtual memory (bytes) snapshot=6560522240
                Total committed heap usage (bytes)=348123136
                Peak Map Physical memory (bytes)=250191872
                Peak Map Virtual memory (bytes)=2186002432
                Peak Reduce Physical memory (bytes)=146477056
                Peak Reduce Virtual memory (bytes)=2191335424
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
                Bytes Written=2673
2026-03-25 23:25:29,691 INFO streaming.StreamJob: Output directory: /user/tanalam/project/m1/task3_sample
tanalam@master-node:~$ hdfs dfs -cat /user/tanalam/project/m1/task3_sample/part-*
ABANDONED BUILDING      2
AIRCRAFT        1
AIRPORT BUILDING NON-TERMINAL - NON-SECURE AREA 2
AIRPORT EXTERIOR - NON-SECURE AREA      2
AIRPORT EXTERIOR - SECURE AREA  3
AIRPORT PARKING LOT     8
AIRPORT TERMINAL LOWER LEVEL - NON-SECURE AREA  5
AIRPORT TERMINAL LOWER LEVEL - SECURE AREA      5
AIRPORT TERMINAL UPPER LEVEL - NON-SECURE AREA  4
AIRPORT TERMINAL UPPER LEVEL - SECURE AREA      11
AIRPORT TRANSPORTATION SYSTEM (ATS)     1
AIRPORT VENDING ESTABLISHMENT   1
AIRPORT/AIRCRAFT        1
ALLEY   216
ANIMAL HOSPITAL 2
APARTMENT       1868
APPLIANCE STORE 5
ATHLETIC CLUB   14
ATM (AUTOMATIC TELLER MACHINE)  8
AUTO    2
AUTO / BOAT / RV DEALERSHIP     9
BANK    37
BAR OR TAVERN   84
BARBERSHOP      5
BOAT / WATERCRAFT       1
BRIDGE  2
BUS     4
CAR WASH        9
CEMETARY        2
CHA APARTMENT   15
CHA HALLWAY / STAIRWELL / ELEVATOR      7
CHA PARKING LOT / GROUNDS       17
CHURCH / SYNAGOGUE / PLACE OF WORSHIP   16
CLEANING STORE  1
COIN OPERATED MACHINE   1
COLLEGE / UNIVERSITY - GROUNDS  3
COLLEGE / UNIVERSITY - RESIDENCE HALL   2
COMMERCIAL / BUSINESS OFFICE    121
CONSTRUCTION SITE       11
CONVENIENCE STORE       51
CREDIT UNION    1
CTA BUS 44
CTA BUS STOP    16
CTA PARKING LOT / GARAGE / OTHER PROPERTY       5
CTA PLATFORM    24
CTA STATION     22
CTA TRACKS - RIGHT OF WAY       3
CTA TRAIN       49
CURRENCY EXCHANGE       6
DAY CARE CENTER 6
DEPARTMENT STORE        134
DRIVEWAY - RESIDENTIAL  25
DRUG STORE      46
FACTORY / MANUFACTURING BUILDING        3
FEDERAL BUILDING        1
FISTS   131
GAS STATION     124
GAS STATION DRIVE/PROP. 1
GOVERNMENT BUILDING / PROPERTY  19
GROCERY FOOD STORE      91
HALLWAY 1
HIGHWAY / EXPRESSWAY    3
HOSPITAL BUILDING / GROUNDS     42
HOTEL / MOTEL   41
HOTEL/MOTEL     3
HOUSE   1
JAIL / LOCK-UP FACILITY 2
LAKEFRONT / WATERFRONT / RIVERBANK      4
LIBRARY 6
MEDICAL / DENTAL OFFICE 11
MOVIE HOUSE / THEATER   5
NURSING / RETIREMENT HOME       42
OTHER   9
OTHER (SPECIFY) 154
OTHER COMMERCIAL TRANSPORTATION 5
OTHER RAILROAD PROPERTY / TRAIN DEPOT   3
PARK PROPERTY   91
PARKING LOT / GARAGE (NON RESIDENTIAL)  355
PAWN SHOP       1
POLICE FACILITY / VEHICLE PARKING LOT   38
PORCH   2
RESIDENCE       1344
RESIDENCE - GARAGE      114
RESIDENCE - PORCH / HALLWAY     100
RESIDENCE - YARD (FRONT / BACK) 126
RESTAURANT      186
RETAIL STORE    1
SCHOOL - PRIVATE BUILDING       13
SCHOOL - PRIVATE GROUNDS        9
SCHOOL - PUBLIC BUILDING        76
SCHOOL - PUBLIC GROUNDS 75
SCOOTER 38
SIDEWALK        524
SMALL RETAIL STORE      234
SPORTS ARENA / STADIUM  13
STREET  2686
TAVERN / LIQUOR STORE   17
TAXICAB 6
VACANT LOT / LAND       30
VEHICLE - COMMERCIAL    10
VEHICLE - DELIVERY TRUCK        1
VEHICLE NON-COMMERCIAL  138
VESTIBULE       1
WAREHOUSE       9
tanalam@master-node:~$ mapred streaming -files mapper_task3.py,reducer_sum.py -mapper "python3 mapper_task3.py" -reducer "python3 reducer_sum.py" -input /data/chicago_crimes.csv -output /user/tanalam/project/m1/task3
packageJobJar: [] [/opt/hadoop-3.4.1/share/hadoop/tools/lib/hadoop-streaming-3.4.1.jar] /tmp/streamjob1044220015855241344.jar tmpDir=null
2026-03-25 23:27:07,651 INFO client.DefaultNoHARMFailoverProxyProvider: Connecting to ResourceManager at master-node/134.209.172.50:8032
2026-03-25 23:27:07,964 INFO client.DefaultNoHARMFailoverProxyProvider: Connecting to ResourceManager at master-node/134.209.172.50:8032
2026-03-25 23:27:08,434 INFO mapreduce.JobResourceUploader: Disabling Erasure Coding for path: /tmp/hadoop-yarn/staging/tanalam/.staging/job_1771402826595_0222
2026-03-25 23:27:10,117 INFO mapred.FileInputFormat: Total input files to process : 1
2026-03-25 23:27:10,156 INFO net.NetworkTopology: Adding a new node: /default-rack/164.92.103.148:9866
2026-03-25 23:27:10,158 INFO net.NetworkTopology: Adding a new node: /default-rack/146.190.147.119:9866
2026-03-25 23:27:10,811 INFO mapreduce.JobSubmitter: number of splits:2
2026-03-25 23:27:11,694 INFO mapreduce.JobSubmitter: Submitting tokens for job: job_1771402826595_0222
2026-03-25 23:27:11,694 INFO mapreduce.JobSubmitter: Executing with tokens: []
2026-03-25 23:27:11,969 INFO conf.Configuration: resource-types.xml not found
2026-03-25 23:27:11,970 INFO resource.ResourceUtils: Unable to find 'resource-types.xml'.
2026-03-25 23:27:12,085 INFO impl.YarnClientImpl: Submitted application application_1771402826595_0222
2026-03-25 23:27:12,136 INFO mapreduce.Job: The url to track the job: http://master-node:8088/proxy/application_1771402826595_0222/
2026-03-25 23:27:12,140 INFO mapreduce.Job: Running job: job_1771402826595_0222
2026-03-25 23:27:31,958 INFO mapreduce.Job: Job job_1771402826595_0222 running in uber mode : false
2026-03-25 23:27:31,960 INFO mapreduce.Job:  map 0% reduce 0%
2026-03-25 23:27:59,422 INFO mapreduce.Job:  map 100% reduce 0%
2026-03-25 23:28:12,795 INFO mapreduce.Job:  map 100% reduce 100%
2026-03-25 23:28:15,635 INFO mapreduce.Job: Job job_1771402826595_0222 completed successfully
2026-03-25 23:28:15,855 INFO mapreduce.Job: Counters: 54
        File System Counters
                FILE: Number of bytes read=12341707
                FILE: Number of bytes written=25626505
                FILE: Number of read operations=0
                FILE: Number of large read operations=0
                FILE: Number of write operations=0
                HDFS: Number of bytes read=181964998
                HDFS: Number of bytes written=4749
                HDFS: Number of read operations=11
                HDFS: Number of large read operations=0
                HDFS: Number of write operations=2
                HDFS: Number of bytes read erasure-coded=0
        Job Counters
                Launched map tasks=2
                Launched reduce tasks=1
                Data-local map tasks=2
                Total time spent by all maps in occupied slots (ms)=95806
                Total time spent by all reduces in occupied slots (ms)=21698
                Total time spent by all map tasks (ms)=47903
                Total time spent by all reduce tasks (ms)=10849
                Total vcore-milliseconds taken by all map tasks=47903
                Total vcore-milliseconds taken by all reduce tasks=10849
                Total megabyte-milliseconds taken by all map tasks=24526336
                Total megabyte-milliseconds taken by all reduce tasks=5554688
        Map-Reduce Framework
                Map input records=793074
                Map output records=793072
                Map output bytes=10755557
                Map output materialized bytes=12341713
                Input split bytes=198
                Combine input records=0
                Combine output records=0
                Reduce input groups=217
                Reduce shuffle bytes=12341713
                Reduce input records=793072
                Reduce output records=216
                Spilled Records=1586144
                Shuffled Maps =2
                Failed Shuffles=0
                Merged Map outputs=2
                GC time elapsed (ms)=853
                CPU time spent (ms)=9120
                Physical memory (bytes) snapshot=676372480
                Virtual memory (bytes) snapshot=6561677312
                Total committed heap usage (bytes)=348266496
                Peak Map Physical memory (bytes)=254320640
                Peak Map Virtual memory (bytes)=2186047488
                Peak Reduce Physical memory (bytes)=169357312
                Peak Reduce Virtual memory (bytes)=2194812928
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
                Bytes Written=4749
2026-03-25 23:28:15,856 INFO streaming.StreamJob: Output directory: /user/tanalam/project/m1/task3
tanalam@master-node:~$ hdfs dfs -cat /user/tanalam/project/m1/task3/part-*
ABANDONED BUILDING      829
AIRCRAFT        34
AIRPORT BUILDING NON-TERMINAL - NON-SECURE AREA 33
AIRPORT BUILDING NON-TERMINAL - SECURE AREA     16
AIRPORT EXTERIOR - NON-SECURE AREA      33
AIRPORT EXTERIOR - SECURE AREA  20
AIRPORT PARKING LOT     81
AIRPORT TERMINAL LOWER LEVEL - NON-SECURE AREA  60
AIRPORT TERMINAL LOWER LEVEL - SECURE AREA      42
AIRPORT TERMINAL MEZZANINE - NON-SECURE AREA    4
AIRPORT TERMINAL UPPER LEVEL - NON-SECURE AREA  41
AIRPORT TERMINAL UPPER LEVEL - SECURE AREA      133
AIRPORT TRANSPORTATION SYSTEM (ATS)     12
AIRPORT VENDING ESTABLISHMENT   7
AIRPORT/AIRCRAFT        2753
ALLEY   18258
ANIMAL HOSPITAL 13
APARTMENT       60925
APPLIANCE STORE 269
ATHLETIC CLUB   465
ATM (AUTOMATIC TELLER MACHINE)  66
AUTO    1370
AUTO / BOAT / RV DEALERSHIP     92
BANK    3325
BAR OR TAVERN   3380
BARBERSHOP      642
BOAT/WATERCRAFT 66
BOWLING ALLEY   85
BRIDGE  28
BUS     3085
CAR WASH        363
CEMETARY        31
CHA APARTMENT   8340
CHA HALLWAY / STAIRWELL / ELEVATOR      60
CHA HALLWAY/STAIRWELL/ELEVATOR  4773
CHA PARKING LOT / GROUNDS       166
CHA PARKING LOT/GROUNDS 11846
CHURCH / SYNAGOGUE / PLACE OF WORSHIP   224
CHURCH/SYNAGOGUE/PLACE OF WORSHIP       1344
CLEANING STORE  786
COIN OPERATED MACHINE   108
COLLEGE / UNIVERSITY - GROUNDS  43
COLLEGE / UNIVERSITY - RESIDENCE HALL   12
COLLEGE/UNIVERSITY GROUNDS      449
COLLEGE/UNIVERSITY RESIDENCE HALL       87
COMMERCIAL / BUSINESS OFFICE    8219
CONSTRUCTION SITE       1206
CONVENIENCE STORE       610
CREDIT UNION    42
CTA BUS 2147
CTA BUS STOP    182
CTA PARKING LOT / GARAGE / OTHER PROPERTY       68
CTA PLATFORM    4938
CTA STATION     185
CTA TRAIN       1932
CURRENCY EXCHANGE       1277
DAY CARE CENTER 246
DELIVERY TRUCK  149
DEPARTMENT STORE        10818
DRIVEWAY - RESIDENTIAL  1902
DRUG STORE      4469
FACTORY / MANUFACTURING BUILDING        53
FACTORY/MANUFACTURING BUILDING  910
FEDERAL BUILDING        85
FIRE STATION    125
FISTS   1157
GAS STATION     7703
GOVERNMENT BUILDING / PROPERTY  365
GOVERNMENT BUILDING/PROPERTY    1447
GROCERY FOOD STORE      13029
HIGHWAY / EXPRESSWAY    13
HIGHWAY/EXPRESSWAY      115
HOSPITAL BUILDING / GROUNDS     552
HOSPITAL BUILDING/GROUNDS       1962
HOTEL / MOTEL   513
HOTEL/MOTEL     3166
HOUSE   675
JAIL / LOCK-UP FACILITY 20
LAKEFRONT / WATERFRONT / RIVERBANK      31
LAKEFRONT/WATERFRONT/RIVERBANK  66
LIBRARY 585
MEDICAL / DENTAL OFFICE 123
MEDICAL/DENTAL OFFICE   753
MOVIE HOUSE / THEATER   47
MOVIE HOUSE/THEATER     297
NURSING / RETIREMENT HOME       311
NURSING HOME/RETIREMENT HOME    1538
OTHER   29213
OTHER (SPECIFY) 1843
OTHER COMMERCIAL TRANSPORTATION 359
OTHER RAILROAD PROP / TRAIN DEPOT       586
OTHER RAILROAD PROPERTY / TRAIN DEPOT   61
PARK PROPERTY   5745
PARKING LOT / GARAGE (NON RESIDENTIAL)  3340
PARKING LOT/GARAGE(NON.RESID.)  21876
POLICE FACILITY / VEHICLE PARKING LOT   415
POLICE FACILITY/VEH PARKING LOT 869
PORCH   398
RESIDENCE       136238
RESIDENCE - GARAGE      1116
RESIDENCE - PORCH / HALLWAY     1270
RESIDENCE - YARD (FRONT / BACK) 964
RESIDENCE PORCH/HALLWAY 12619
RESIDENCE-GARAGE        14266
RESTAURANT      11996
SCHOOL - PRIVATE BUILDING       123
SCHOOL - PRIVATE GROUNDS        148
SCHOOL - PUBLIC BUILDING        803
SCHOOL - PUBLIC GROUNDS 759
SCOOTER 477
SIDEWALK        47407
SMALL RETAIL STORE      13755
SPORTS ARENA / STADIUM  84
SPORTS ARENA/STADIUM    349
STREET  245437
TAVERN / LIQUOR STORE   238
TAVERN/LIQUOR STORE     3764
TAXICAB 701
VACANT LOT / LAND       346
VACANT LOT/LAND 1892
VEHICLE - COMMERCIAL    107
VEHICLE NON-COMMERCIAL  7738
VEHICLE-COMMERCIAL      435
WAREHOUSE       1286
YARD    311
tanalam@master-node:~$
```

</details>

---

### Task 4: Year Trend Analysis
**Research Question:** How has the total number of crimes changed over the years?

**Mapper logic:** Extract `parts[2]` (Date), split by space to get date portion, split by `/` to get year at index 2, emit `(year, 1)` for every record.

**MapReduce Command (Sample):**
```bash
mapred streaming \
  -files mapper_task4.py,reducer_sum.py \
  -mapper "python3 mapper_task4.py" \
  -reducer "python3 reducer_sum.py" \
  -input /data/chicago_crimes_sample.csv \
  -output /user/mhussen/project/m1/task4_sample
```

**MapReduce Command (Full Dataset):**
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
| 2001 | 467,301 |
| 2002 | 205,267 |
| 2023 | 81,461 |
| 2025 | 12,710 |
| 2022 | 4,678 |

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

**Mapper logic:** Extract `parts[8]` (Arrest), apply `.lower()` for case safety, emit `"Arrested\t1"` if true, `"Not Arrested\t1"` otherwise, for every record.

**MapReduce Command (Sample):**
```bash
mapred streaming \
  -files mapper_task5.py,reducer_sum.py \
  -mapper "python3 mapper_task5.py" \
  -reducer "python3 reducer_sum.py" \
  -input /data/chicago_crimes_sample.csv \
  -output /user/bothman/project/m1/task5_sample
```

**MapReduce Command (Full Dataset):**
```bash
mapred streaming \
  -files mapper_task5.py,reducer_sum.py \
  -mapper "python3 mapper_task5.py" \
  -reducer "python3 reducer_sum.py" \
  -input /data/chicago_crimes.csv \
  -output /user/bothman/project/m1/task5
```

**Results:**

| Status | Count | Percentage |
|--------|-------|------------|
| Not Arrested | 577,873 | 72.9% |
| Arrested | 215,199 | 27.1% |
| **Total** | **793,072** | **100%** |

**Interpretation:** Only 27.1% of crimes in Chicago result in an arrest, meaning nearly 3 out of 4 crimes go without an arrest. This indicates a significant gap in law enforcement follow-through and suggests that patrol efficiency and investigative capacity may need to be reviewed, particularly for the most common crime types like Theft and Criminal Damage where arrest rates tend to be lower.

**Execution Log:**

<details>
<summary>Click to expand full execution log</summary>
```
bothman@master-node:~$ mapred streaming -files mapper_task5.py,reducer_sum.py -mapper "python3 mapper_task5.py" -reducer "python3 reducer_sum.py" -input /data/chicago_crimes_sample.csv -output /user/bothman/project/m1/task5_sample
packageJobJar: [] [/opt/hadoop-3.4.1/share/hadoop/tools/lib/hadoop-streaming-3.4.1.jar] /tmp/streamjob16716504823601346957.jar tmpDir=null
2026-03-26 14:13:50,256 INFO client.DefaultNoHARMFailoverProxyProvider: Connecting to ResourceManager at master-node/134.209.172.50:8032
2026-03-26 14:13:50,623 INFO client.DefaultNoHARMFailoverProxyProvider: Connecting to ResourceManager at master-node/134.209.172.50:8032
2026-03-26 14:13:51,100 INFO mapreduce.JobResourceUploader: Disabling Erasure Coding for path: /tmp/hadoop-yarn/staging/bothman/.staging/job_1771402826595_0233
2026-03-26 14:13:52,789 INFO mapred.FileInputFormat: Total input files to process : 1
2026-03-26 14:13:53,444 INFO mapreduce.JobSubmitter: number of splits:2
2026-03-26 14:13:54,389 INFO mapreduce.JobSubmitter: Submitting tokens for job: job_1771402826595_0233
2026-03-26 14:13:54,389 INFO mapreduce.JobSubmitter: Executing with tokens: []
2026-03-26 14:13:54,781 INFO conf.Configuration: resource-types.xml not found
2026-03-26 14:13:54,782 INFO resource.ResourceUtils: Unable to find 'resource-types.xml'.
2026-03-26 14:13:54,911 INFO impl.YarnClientImpl: Submitted application application_1771402826595_0233
2026-03-26 14:13:54,966 INFO mapreduce.Job: The url to track the job: http://master-node:8088/proxy/application_1771402826595_0233/
2026-03-26 14:13:54,968 INFO mapreduce.Job: Running job: job_1771402826595_0233
2026-03-26 14:14:14,757 INFO mapreduce.Job: Job job_1771402826595_0233 running in uber mode : false
2026-03-26 14:14:14,759 INFO mapreduce.Job:  map 0% reduce 0%
2026-03-26 14:14:35,304 INFO mapreduce.Job:  map 100% reduce 0%
2026-03-26 14:14:48,427 INFO mapreduce.Job:  map 100% reduce 100%
2026-03-26 14:14:51,184 INFO mapreduce.Job: Job job_1771402826595_0233 completed successfully
2026-03-26 14:14:51,387 INFO mapreduce.Job: Counters: 54
        File System Counters
                FILE: Number of bytes read=165126
                FILE: Number of bytes written=1273388
                FILE: Number of read operations=0
                FILE: Number of large read operations=0
                FILE: Number of write operations=0
                HDFS: Number of bytes read=2391502
                HDFS: Number of bytes written=32
                HDFS: Number of read operations=11
                HDFS: Number of large read operations=0
                HDFS: Number of write operations=2
                HDFS: Number of bytes read erasure-coded=0
        Job Counters
                Launched map tasks=2
                Launched reduce tasks=1
                Data-local map tasks=2
                Total time spent by all maps in occupied slots (ms)=69050
                Total time spent by all reduces in occupied slots (ms)=18946
                Total time spent by all map tasks (ms)=34525
                Total time spent by all reduce tasks (ms)=9473
                Total vcore-milliseconds taken by all map tasks=34525
                Total vcore-milliseconds taken by all reduce tasks=9473
                Total megabyte-milliseconds taken by all map tasks=17676800
                Total megabyte-milliseconds taken by all reduce tasks=4850176
        Map-Reduce Framework
                Map input records=10001
                Map output records=10000
                Map output bytes=145120
                Map output materialized bytes=165132
                Input split bytes=212
                Combine input records=0
                Combine output records=0
                Reduce input groups=2
                Reduce shuffle bytes=165132
                Reduce input records=10000
                Reduce output records=2
                Spilled Records=20000
                Shuffled Maps =2
                Failed Shuffles=0
                Merged Map outputs=2
                GC time elapsed (ms)=716
                CPU time spent (ms)=3310
                Physical memory (bytes) snapshot=640094208
                Virtual memory (bytes) snapshot=6556971008
                Total committed heap usage (bytes)=348160000
                Peak Map Physical memory (bytes)=250064896
                Peak Map Virtual memory (bytes)=2184417280
                Peak Reduce Physical memory (bytes)=143462400
                Peak Reduce Virtual memory (bytes)=2189180928
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
                Bytes Written=32
2026-03-26 14:14:51,387 INFO streaming.StreamJob: Output directory: /user/bothman/project/m1/task5_sample
bothman@master-node:~$ hdfs dfs -cat /user/bothman/project/m1/task5_sample/part-*
Arrested        1220
Not Arrested    8780
bothman@master-node:~$ mapred streaming -files mapper_task5.py,reducer_sum.py -mapper "python3 mapper_task5.py" -reducer "python3 reducer_sum.py" -input /data/chicago_crimes.csv -output /user/bothman/project/m1/task5
packageJobJar: [] [/opt/hadoop-3.4.1/share/hadoop/tools/lib/hadoop-streaming-3.4.1.jar] /tmp/streamjob4978979378508820736.jar tmpDir=null
2026-03-26 14:15:12,466 INFO client.DefaultNoHARMFailoverProxyProvider: Connecting to ResourceManager at master-node/134.209.172.50:8032
2026-03-26 14:15:12,902 INFO client.DefaultNoHARMFailoverProxyProvider: Connecting to ResourceManager at master-node/134.209.172.50:8032
2026-03-26 14:15:13,387 INFO mapreduce.JobResourceUploader: Disabling Erasure Coding for path: /tmp/hadoop-yarn/staging/bothman/.staging/job_1771402826595_0234
2026-03-26 14:15:15,217 INFO mapred.FileInputFormat: Total input files to process : 1
2026-03-26 14:15:15,247 INFO net.NetworkTopology: Adding a new node: /default-rack/146.190.147.119:9866
2026-03-26 14:15:15,248 INFO net.NetworkTopology: Adding a new node: /default-rack/164.92.103.148:9866
2026-03-26 14:15:15,920 INFO mapreduce.JobSubmitter: number of splits:2
2026-03-26 14:15:16,817 INFO mapreduce.JobSubmitter: Submitting tokens for job: job_1771402826595_0234
2026-03-26 14:15:16,817 INFO mapreduce.JobSubmitter: Executing with tokens: []
2026-03-26 14:15:17,216 INFO conf.Configuration: resource-types.xml not found
2026-03-26 14:15:17,218 INFO resource.ResourceUtils: Unable to find 'resource-types.xml'.
2026-03-26 14:15:17,339 INFO impl.YarnClientImpl: Submitted application application_1771402826595_0234
2026-03-26 14:15:17,400 INFO mapreduce.Job: The url to track the job: http://master-node:8088/proxy/application_1771402826595_0234/
2026-03-26 14:15:17,408 INFO mapreduce.Job: Running job: job_1771402826595_0234
2026-03-26 14:15:35,115 INFO mapreduce.Job: Job job_1771402826595_0234 running in uber mode : false
2026-03-26 14:15:35,116 INFO mapreduce.Job:  map 0% reduce 0%
2026-03-26 14:16:02,476 INFO mapreduce.Job:  map 100% reduce 0%
2026-03-26 14:16:18,281 INFO mapreduce.Job:  map 100% reduce 100%
2026-03-26 14:16:22,366 INFO mapreduce.Job: Job job_1771402826595_0234 completed successfully
2026-03-26 14:16:22,611 INFO mapreduce.Job: Counters: 54
        File System Counters
                FILE: Number of bytes read=12621434
                FILE: Number of bytes written=26185959
                FILE: Number of read operations=0
                FILE: Number of large read operations=0
                FILE: Number of write operations=0
                HDFS: Number of bytes read=181964998
                HDFS: Number of bytes written=36
                HDFS: Number of read operations=11
                HDFS: Number of large read operations=0
                HDFS: Number of write operations=2
                HDFS: Number of bytes read erasure-coded=0
        Job Counters
                Launched map tasks=2
                Launched reduce tasks=1
                Data-local map tasks=2
                Total time spent by all maps in occupied slots (ms)=99516
                Total time spent by all reduces in occupied slots (ms)=25786
                Total time spent by all map tasks (ms)=49758
                Total time spent by all reduce tasks (ms)=12893
                Total vcore-milliseconds taken by all map tasks=49758
                Total vcore-milliseconds taken by all reduce tasks=12893
                Total megabyte-milliseconds taken by all map tasks=25476096
                Total megabyte-milliseconds taken by all reduce tasks=6601216
        Map-Reduce Framework
                Map input records=793074
                Map output records=793072
                Map output bytes=11035284
                Map output materialized bytes=12621440
                Input split bytes=198
                Combine input records=0
                Combine output records=0
                Reduce input groups=2
                Reduce shuffle bytes=12621440
                Reduce input records=793072
                Reduce output records=2
                Spilled Records=1586144
                Shuffled Maps =2
                Failed Shuffles=0
                Merged Map outputs=2
                GC time elapsed (ms)=861
                CPU time spent (ms)=9580
                Physical memory (bytes) snapshot=676519936
                Virtual memory (bytes) snapshot=6561419264
                Total committed heap usage (bytes)=348119040
                Peak Map Physical memory (bytes)=271200256
                Peak Map Virtual memory (bytes)=2188054528
                Peak Reduce Physical memory (bytes)=153047040
                Peak Reduce Virtual memory (bytes)=2189737984
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
                Bytes Written=36
2026-03-26 14:16:22,611 INFO streaming.StreamJob: Output directory: /user/bothman/project/m1/task5
bothman@master-node:~$ hdfs dfs -cat /user/bothman/project/m1/task5/part-*
Arrested        215199
Not Arrested    577873
bothman@master-node:~$
```

</details>

---

## Member Contributions

| Name                    | Contribution                                                                                      |
|-------------------------|---------------------------------------------------------------------------------------------------|
| Ahmad Fares Mzayek      | Created and structured the GitHub repository, managed branch strategy, reviewed and merged all PRs |
| Faisal Hajj Khalil      | Wrote mapper_task2.py for crime type distribution, executed both sample and full dataset runs on the cluster, committed code and results |
| Tanzim Alam             | Wrote mapper_task3.py for location hotspot analysis, executed both sample and full dataset runs on the cluster, committed code and results |
| Mohammad Ghassan Hussen | Wrote mapper_task4.py for year trend analysis, executed both sample and full dataset runs on the cluster, committed code and results |
| Bilal Othman            | Wrote mapper_task5.py for arrest analysis, executed both sample and full dataset runs on the cluster, committed code and results |

---

*SE446 Big Data Engineering — Group Project*
