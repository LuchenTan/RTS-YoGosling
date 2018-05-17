### Results on RTS17 collection

#### 1. ```config/producer.ini``` ```[ARCHIVE]``` setting:
```commandline
raw_topic = tweets_archive_raw
processed_topic_crawled = tweets_archive
processed_topic_nocrawl = tweets_archive_nocrawl
keyword = all
batchsize = 50000
startpoint = 1501286400000
endpoint = 1501977599000
location = /media/l8tan/Data/TweetArchive/RTS2017
```

#### 2. ```config/runs.ini``` ```[PROFILE]``` setting:
```
location = /home/l8tan/Projects/RTS-YoGosling/profiles/
year = 17
```
#### 3. Runs

* rm: Title Match; sim: None; window size: 0
```commandline
python3 Runs/start_run.py -s archive -r RUNA --no-crawl-url -o results/rts17_title_noSim_window0.txt -m title -d None
python3 eval_scripts/get_eval.py -y 17 -r ../results/rts17_title_noSim_window0.txt
```
Mobile Assessment Results: 

'run                                     	topic	relevant	redundant	not_relevant	unjudgedtotal_length	coverage	mean_latency	median_latency	strict-p	lenient-p	online_utility(strict)	online_utility(lenient)'

'RunA	All	1359	252	1555	911	2610	0.651	1.0	1.0	**0.4292**	**0.5088**	-448	56'

Batch Assessment Results:

'runtag	topic	EGp   	EG1   	nCGp  	nCG1  	GMP.33    	GMP.50    	GMP.66    	mean_latency   	median_latency 	total_length'

'RunA	All  	**0.2419**	0.2193	**0.2653**	0.2426	-0.4261   	-0.2619   	-0.1074   	24617.2        1.0            	857'

* rm: Title Match; sim: None; window size: 1hr

```commandline
python3 Runs/start_run.py -s archive -r RUNA --no-crawl-url -o results/rts17_title_noSim_window1hr.txt -m title -d None -w 3600
python3 eval_scripts/get_eval.py -y 17 -r ../results/rts17_title_noSim_window1hr.txt
```
Mobile Assessment Results: 

'run                                     	topic	relevant	redundant	not_relevant	unjudged	total_length	coverage	mean_latency	median_latency	strict-p	lenient-p	online_utility(strict)	online_utility(lenient)'

'RUNA	All	1112	205	1261	816	2192	0.628	1.0	1.0	**0.4313**	**0.5109**	-354	56'

Batch Assessment Results:

'runtag	topic	EGp   	EG1   	nCGp  	nCG1  	GMP.33    	GMP.50    	GMP.66    	mean_latency   	median_latency 	total_length'

'RUNA	All  	**0.2464**	0.2222	**0.2580**	0.2338	-0.3202   	-0.1891   	-0.0657   	28314.6        	1.0            	691'

* rm: Title Match; sim: None; window size; 2hrs

```commandline
python3 Runs/start_run.py -s archive -r RUNA --no-crawl-url -o results/rts17_title_noSim_window2hr.txt -m title -d None -w 7200
python3 eval_scripts/get_eval.py -y 17 -r ../results/rts17_title_noSim_window2hr.txt
```
Mobile Assessment Results: 

'run                                     	topic	relevant	redundant	not_relevant	unjudged	total_length	coverage	mean_latency	median_latency	strict-p	lenient-p	online_utility(strict)	online_utility(lenient)'

'RUNA	All	928	180	1055	697	1858	0.625	1.0	1.0	**0.429**	**0.5123**	-307	53'
Batch Assessment Results:

'runtag	topic	EGp   	EG1   	nCGp  	nCG1  	GMP.33    	GMP.50    	GMP.66    	mean_latency   	median_latency 	total_length'

'RUNA	All  	**0.2490**	0.2257	**0.2506**	0.2273	-0.2461   	-0.1385   	-0.0373   	40151.1        	1.0            	571'


* rm: Title Match; sim: jaccard 0.6; window size; 0

```commandline
python3 Runs/start_run.py -s archive -r RUNA --no-crawl-url -o results/rts17_title_jaccard0.6_window0.txt -m title -d jaccard -U 0.6 -w 0
python3 eval_scripts/get_eval.py -y 17 -r ../results/rts17_title_jaccard0.6_window0.txt
```
Mobile Assessment Results: 

'run                                     	topic	relevant	redundant	not_relevant	unjudged	total_length	coverage	mean_latency	median_latency	strict-p	lenient-p	online_utility(strict)	online_utility(lenient)'

'RUNA	All	1311	227	1561	598	2249	0.734	1.0	1.0	**0.423**	**0.4963**	-477	-23'
Batch Assessment Results:

'runtag	topic	EGp   	EG1   	nCGp  	nCG1  	GMP.33    	GMP.50    	GMP.66    	mean_latency   	median_latency 	total_length'

'RUNA	All  	**0.2518**	0.2297	**0.2693**	0.2473	-0.3182   	-0.1794   	-0.0488   	22901.3        	1.0            	748'

* rm: Title Match; sim: jaccard 0.8; window size; 0
```commandline
python3 Runs/start_run.py -s archive -r RUNA --no-crawl-url -o results/rts17_title_jaccard0.8_window0.txt -m title -d jaccard -U 0.8 -w 0
python3 eval_scripts/get_eval.py -y 17 -r ../results/rts17_title_jaccard0.8_window0.txt
```
Mobile Assessment Results: 

'run                                     	topic	relevant	redundant	not_relevant	unjudged	total_length	coverage	mean_latency	median_latency	strict-p	lenient-p	online_utility(strict)	online_utility(lenient)'

'RUNA	All	1347	235	1568	607	2287	0.735	1.0	1.0	**0.4276**	**0.5022**	-456	14'
Batch Assessment Results:

'runtag	topic	EGp   	EG1   	nCGp  	nCG1  	GMP.33    	GMP.50    	GMP.66    	mean_latency   	median_latency 	total_length'

'RUNA	All  	**0.2509**	0.2281	**0.2688**	0.2460	-0.3329   	-0.1904   	-0.0563   	23153.5        	1.0            	764'

* rm: Title Match; sim; jaccard 0.6; window size; 1hrs
```commandline
python3 Runs/start_run.py -s archive -r RUNA --no-crawl-url -o results/rts17_title_jaccard0.6_window1hr.txt -m title -d jaccard -U 0.6 -w 3600
python3 eval_scripts/get_eval.py -y 17 -r ../results/rts17_title_jaccard0.6_window1hr.txt
```
Mobile Assessment Results: 

'run                                     	topic	relevant	redundant	not_relevant	unjudged	total_length	coverage	mean_latency	median_latency	strict-p	lenient-p	online_utility(strict)	online_utility(lenient)'

'RUNA	All	1072	171	1287	598	1938	0.691	1.0	1.0	**0.4237**	**0.4913**	-386	-44'
Batch Assessment Results:

'runtag	topic	EGp   	EG1   	nCGp  	nCG1  	GMP.33    	GMP.50    	GMP.66    	mean_latency   	median_latency 	total_length'

'RUNA	All  	**0.2533**	0.2315	**0.2626**	0.2408	-0.2553   	-0.1379   	-0.0274   	26843.3        	1.0            	634'

* rm: Title Counting 0.7; sim; None; window size: 0
```commandline
python3 Runs/start_run.py -s archive -r RUNA --no-crawl-url -o results/rts17_simpleCount0.7_noSim_window0.txt -m simpleCount -T 0.7 -d None -w 0
python3 eval_scripts/get_eval.py -y 17 -r ../results/rts17_simpleCount0.7_noSim_window0.txt
```
Mobile Assessment Results: 

'run                                     	topic	relevant	redundant	not_relevant	unjudged	total_length	coverage	mean_latency	median_latency	strict-p	lenient-p	online_utility(strict)	online_utility(lenient)'

'RUNA	All	1469	300	1749	1003	2910	0.655	1.0	1.0	**0.4176	0.5028**	-580	20'

Batch Assessment Results:

'runtag	topic	EGp   	EG1   	nCGp  	nCG1  	GMP.33    	GMP.50    	GMP.66    	mean_latency   	median_latency 	total_length'

'RUNA	All  	**0.2529	0.2291	0.2729**	0.2490	-0.4566   	-0.2809   	-0.1156   	30630.8        	1.0            	915'


* rm: Title Counting 0.7; sim: None; window size: 1hr
```commandline
python3 Runs/start_run.py -s archive -r RUNA --no-crawl-url -o results/rts17_simpleCount0.7_noSim_window1hr.txt -m simpleCount -T 0.7 -d None -w 3600
python3 eval_scripts/get_eval.py -y 17 -r ../results/rts17_simpleCount0.7_noSim_window1hr.txt
```
Mobile Assessment Results: 

'run                                     	topic	relevant	redundant	not_relevant	unjudged	total_length	coverage	mean_latency	median_latency	strict-p	lenient-p	online_utility(strict)	online_utility(lenient)'

'RUNA	All	1202	246	1401	882	2419	0.635	1.0	1.0	**0.4219	0.5082**	-445	47'

Batch Assessment Results:

'runtag	topic	EGp   	EG1   	nCGp  	nCG1  	GMP.33    	GMP.50    	GMP.66    	mean_latency   	median_latency 	total_length'

'RUNA	All  	**0.2583	0.2329	0.2657**	0.2403	-0.3386   	-0.1991   	-0.0678   	35080.2        	1.0            	735'

* rm: Title Counting 0.7; sim: jaccard 0.6; window size: 0
```commandline
python3 Runs/start_run.py -s archive -r RUNA --no-crawl-url -o results/rts17_simpleCount0.7_jaccard0.6_window0.txt -m simpleCount -T 0.7 -d jaccard -U 0.6 -w 0
python3 eval_scripts/get_eval.py -y 17 -r ../results/rts17_simpleCount0.7_jaccard0.6_window0.txt
```
Mobile Assessment Results: 

'run                                     	topic	relevant	redundant	not_relevant	unjudged	total_length	coverage	mean_latency	median_latency	strict-p	lenient-p	online_utility(strict)	online_utility(lenient)'

'RUNA	All	1427	265	1734	658	2499	0.737	1.0	1.0	**0.4165	0.4939**	-572	-42'

Batch Assessment Results:

'runtag	topic	EGp   	EG1   	nCGp  	nCG1  	GMP.33    	GMP.50    	GMP.66    	mean_latency   	median_latency 	total_length'

'RUNA	All  	**0.2637	0.2405	0.2769**	0.2537	-0.3341   	-0.1875   	-0.0496   	28756.2        	1.0            	789'

* rm: Title Counting 0.7; sim: jaccard 0.6; window size: 1hr
```commandline
python3 Runs/start_run.py -s archive -r RUNA --no-crawl-url -o results/rts17_simpleCount0.7_jaccard0.6_window1hr.txt -m simpleCount -T 0.7 -d jaccard -U 0.6 -w 3600
python3 eval_scripts/get_eval.py -y 17 -r ../results/rts17_simpleCount0.7_jaccard0.6_window1hr.txt
```
Mobile Assessment Results: 

'run                                     	topic	relevant	redundant	not_relevant	unjudged	total_length	coverage	mean_latency	median_latency	strict-p	lenient-p	online_utility(strict)	online_utility(lenient)'

'RUNA	All	1165	208	1407	657	2143	0.693	1.0	1.0	**0.4191	0.4939**	-450	-34'

Batch Assessment Results:

'runtag	topic	EGp   	EG1   	nCGp  	nCG1  	GMP.33    	GMP.50    	GMP.66    	mean_latency   	median_latency 	total_length'

'RUNA	All  	**0.2657	0.2427	0.2702**	0.2473	-0.2686   	-0.1440   	-0.0268   	33356.3        	1.0            	672'

### 4. Summary Table

| Run                                       | Mobile Coverage | strict-p | lenient-p | EG-p     | nCGp      |
| ------------------------------------------|-----------------|----------|-----------|----------|-----------|
| Title match, no similarity, window 0      | 0.651           | 0.4292   | 0.5088    | 0.2419   | 0.2653    |
| Title match, no similarity, window 1hr    | 0.628           | **0.4313**   | 0.5109    | 0.2464   | 0.2580    |
| Title match, no similarity, window 2hrs   | 0.625           | 0.429    | **0.5123**    | 0.2490   | 0.2506    |
| Title match, Jaccard 0.6, window 0        | 0.734           | 0.423    | 0.4963    | 0.2518   | 0.2693    | 
| Title match, Jaccard 0.8, window 0        | 0.735           | 0.4276   | 0.5022    | 0.2509   | 0.2688    | 
| Title match, Jaccard 0.6, window 1hr      | 0.691           | 0.4237   | 0.4913    | 0.2533   | 0.2626    |
| Title Ratio 0.7, no similarity, window 0  | 0.655           | 0.4176	  | 0.5028    | 0.2529   | **0.2729**    |
| Title Ratio 0.7, no similarity, window 1hr| 0.635           | 0.4219	  | 0.5082    | 0.2583   | 0.2657    |
| Title Ratio 0.7, Jaccard 0.6, window 0    | **0.737**           | 0.4165	  | 0.4939    | 0.2637	  | 0.2769    |
| Title Ratio 0.7, Jaccard 0.6, window 1hr  | 0.693           | 0.4191	  | 0.4939    | **0.2657**   | 0.2702    |
