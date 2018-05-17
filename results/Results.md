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
```
* rm: Title Match; sim: None; window size: 1hr

```commandline
python3 Runs/start_run.py -s archive -r RUNA --no-crawl-url -o results/rts17_title_noSim_window1hr.txt -m title -d None -w 3600
```

* rm: Title Match; sim: None; window size; 2hrs

```commandline
python3 Runs/start_run.py -s archive -r RUNA --no-crawl-url -o results/rts17_title_noSim_window2hr.txt -m title -d None -w 7200
```

* rm: Title Match; sim: jaccard 0.6; window size; 0

```commandline
python3 Runs/start_run.py -s archive -r RUNA --no-crawl-url -o results/rts17_title_jaccard0.6_window0.txt -m title -d jaccard -U 0.6 -w 0
```

* rm: Title Match; sim: jaccard 0.8; window size; 0
```commandline
python3 Runs/start_run.py -s archive -r RUNA --no-crawl-url -o results/rts17_title_jaccard0.8_window0.txt -m title -d jaccard -U 0.8 -w 0
```

* rm: Title Match; sim; jaccard 0.6; window size; 1hrs
```commandline
python3 Runs/start_run.py -s archive -r RUNA --no-crawl-url -o results/rts17_title_jaccard0.6_window1hr.txt -m title -d jaccard -U 0.6 -w 3600
```
* rm: Title Counting; sim; None; window size: 0
```commandline
python3 Runs/start_run.py -s archive -r RUNA --no-crawl-url -o results/rts17_simpleCount_noSim_window0.txt -m simpleCount -d None -w 0
```
* rm: Title Counting; sim: None; window size: 1hr
```commandline
python3 Runs/start_run.py -s archive -r RUNA --no-crawl-url -o results/rts17_simpleCount_noSim_window3600.txt -m simpleCount -d None -w 3600
```
* rm: Title Counting; sim: jaccard 0.6; window size: 0
```commandline
python3 Runs/start_run.py -s archive -r RUNA --no-crawl-url -o results/rts17_simpleCount_jaccard0.6_window0.txt -m simpleCount -d jaccard -U 0.6 -w 0
```
* rm: Title Counting; sim: jaccard 0.6; window size: 1hr
```commandline
python3 Runs/start_run.py -s archive -r RUNA --no-crawl-url -o results/rts17_simpleCount_jaccard0.6_window1hr.txt -m simpleCount -d jaccard -U 0.6 -w 3600
```

#### Table
