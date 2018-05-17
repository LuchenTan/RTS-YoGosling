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
* rm: Title Match; sim: None; window size: 1hr

```commandline
python3 Runs/start_run.py -s archive -r RUNA --no-crawl-url -o results/rts17_title_noSim_window1hr.txt -m title -d None -w 3600
python3 eval_scripts/get_eval.py -y 17 -r ../results/rts17_title_noSim_window1hr.txt
```

* rm: Title Match; sim: None; window size; 2hrs

```commandline
python3 Runs/start_run.py -s archive -r RUNA --no-crawl-url -o results/rts17_title_noSim_window2hr.txt -m title -d None -w 7200
python3 eval_scripts/get_eval.py -y 17 -r ../results/rts17_title_noSim_window2hr.txt
```

* rm: Title Match; sim: jaccard 0.6; window size; 0

```commandline
python3 Runs/start_run.py -s archive -r RUNA --no-crawl-url -o results/rts17_title_jaccard0.6_window0.txt -m title -d jaccard -U 0.6 -w 0
python3 eval_scripts/get_eval.py -y 17 -r ../results/rts17_title_jaccard0.6_window0.txt
```

* rm: Title Match; sim: jaccard 0.8; window size; 0
```commandline
python3 Runs/start_run.py -s archive -r RUNA --no-crawl-url -o results/rts17_title_jaccard0.8_window0.txt -m title -d jaccard -U 0.8 -w 0
python3 eval_scripts/get_eval.py -y 17 -r ../results/rts17_title_jaccard0.8_window0.txt
```

* rm: Title Match; sim; jaccard 0.6; window size; 1hrs
```commandline
python3 Runs/start_run.py -s archive -r RUNA --no-crawl-url -o results/rts17_title_jaccard0.6_window1hr.txt -m title -d jaccard -U 0.6 -w 3600
python3 eval_scripts/get_eval.py -y 17 -r ../results/rts17_title_jaccard0.6_window1hr.txt
```
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

#### Table
