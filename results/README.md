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

* rm: Title Counting; sim; None; window size: 0
```commandline
python3 Runs/start_run.py -s archive -r RUNA --no-crawl-url -o results/rts17_simpleCount_noSim_window0.txt -m simpleCount -d None -w 0
python3 eval_scripts/get_eval.py -y 17 -r ../results/rts17_simpleCount_noSim_window0.txt
```
Mobile Assessment Results: 

'run                                     	topic	relevant	redundant	not_relevant	unjudgedtotal_length	coverage	mean_latency	median_latency	strict-p	lenient-p	online_utility(strict)	online_utility(lenient)'

'RUNA	All	540	133	930	14640	15511	0.056	1.0	1.0	**0.3369**	**0.4198**	-523	-257'

Batch Assessment Results:

'runtag	topic	EGp   	EG1   	nCGp  	nCG1  	GMP.33    	GMP.50    	GMP.66    	mean_latency   	median_latency 	total_length'

'RUNA	All  	**0.1978**	0.1276	**0.2101**	0.1399	-0.6845   	-0.4768   	-0.2813   	12417.3        1.0            	1022'


* rm: Title Counting; sim: None; window size: 1hr
```commandline
python3 Runs/start_run.py -s archive -r RUNA --no-crawl-url -o results/rts17_simpleCount_noSim_window3600.txt -m simpleCount -d None -w 3600
python3 eval_scripts/get_eval.py -y 17 -r ../results/rts17_simpleCount_noSim_window3600.txt
```
Mobile Assessment Results: 

'run                                     	topic	relevant	redundant	not_relevant	unjudged	total_length	coverage	mean_latency	median_latency	strict-p	lenient-p	online_utility(strict)	online_utility(lenient)'

'RUNA	All	1139	242	1614	9715	11344	0.144	1.0	1.0	**0.3803**	**0.4611**	-717	-233'
Batch Assessment Results:

'runtag	topic	EGp   	EG1   	nCGp  	nCG1  	GMP.33    	GMP.50    	GMP.66    	mean_latency   	median_latency 	total_length'

'RUNA	All  	**0.2310**	0.1425	**0.2435**	0.1550	-0.8741   	-0.5921   	-0.3268   	50952.7        	1.0            	1410'

* rm: Title Counting; sim: jaccard 0.6; window size: 0
```commandline
python3 Runs/start_run.py -s archive -r RUNA --no-crawl-url -o results/rts17_simpleCount_jaccard0.6_window0.txt -m simpleCount -d jaccard -U 0.6 -w 0
python3 eval_scripts/get_eval.py -y 17 -r ../results/rts17_simpleCount_jaccard0.6_window0.txt
```

Mobile Assessment Results: 

'run                                     	topic	relevant	redundant	not_relevant	unjudgedtotal_length	coverage	mean_latency	median_latency	strict-p	lenient-p	online_utility(strict)	online_utility(lenient)'

'RUNA	All	573	131	1008	14505	15431	0.06	1.0	1.0	**0.3347**	**0.4112**	-566	-304'

Batch Assessment Results:

'runtag	topic	EGp   	EG1   	nCGp  	nCG1  	GMP.33    	GMP.50    	GMP.66    	mean_latency   	median_latency 	total_length'

'RUNA	All  	**0.2026**	0.1308	**0.2152**	0.1435	-0.7044   	-0.4878   	-0.2838   	14464.6        1.0            	1072'


* rm: Title Counting; sim: jaccard 0.6; window size: 1hr
```commandline
python3 Runs/start_run.py -s archive -r RUNA --no-crawl-url -o results/rts17_simpleCount_jaccard0.6_window1hr.txt -m simpleCount -d jaccard -U 0.6 -w 3600
python3 eval_scripts/get_eval.py -y 17 -r ../results/rts17_simpleCount_jaccard0.6_window1hr.txt
```
Mobile Assessment Results: 

'run                                     	topic	relevant	redundant	not_relevant	unjudged	total_length	coverage	mean_latency	median_latency	strict-p	lenient-p	online_utility(strict)	online_utility(lenient)'

'RUNA	All	1110	232	1613	9673	11305	0.144	1.0	1.0	**0.3756**	**0.4541**	-735	-271'
Batch Assessment Results:

'runtag	topic	EGp   	EG1   	nCGp  	nCG1  	GMP.33    	GMP.50    	GMP.66    	mean_latency   	median_latency 	total_length'

'RUNA	All  	**0.2350**	0.1473	**0.2433**	0.1555	-0.8152   	-0.5474   	-0.2953   	49340.0        	1.0            	1347'

#### Table
