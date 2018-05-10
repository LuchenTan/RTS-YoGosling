# RTS-YoGosling

RTS-YoGosling is a Python project running under the scenario of [TREC Real-Time Summarization (RTS) Track](http://trecrts.github.io/).

The official RTS track participating system will "listen" to the Twitter sample stream using the Twitter streaming API. To help replay the system after the official evaluation period of RTS, we also support reading from an 
archive file from disk. 

Here is our system overview.

![Overview](overview.jpg)


## 1. Installation
### Installing Kafka:
Our system is using Kafka to store tweet candidates. Thus, Kafka needs to be installed and started before running.

Kafka installation follows **Step 1** [here](https://kafka.apache.org/quickstart). 
### Package Requirements:
* [twython](https://twython.readthedocs.io/en/latest/): Python wrapper for the Twitter API. Supports both normal and streaming Twitter APIs.
* [NLTK](https://www.nltk.org/): Natural Language Toolkit.
* [kafka-python](https://github.com/dpkp/kafka-python): Python client for the Apache Kafka distributed stream processing system.
* [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/): Python library for pulling data out of HTML and XML files.
* [certifi](https://github.com/certifi/python-certifi): Curated collection of Root Certificates for validating the trustworthiness of SSL certificates while verifying the identity of TLS hosts.
* [sklearn](http://scikit-learn.org/stable/): Python Maching Learning tools
## 2. Starting Kafka Service

Before starting Kafka Service, some configuration on the server should be done for running our system.

Go to the Kafka folder, write the following lines to ```config/server.properties``` file.

```commandline
> log.retention.hours=-1
> delete.topic.enable=True 
> auto.create.topics.enable=True
```

Then following **Step 2** [here](https://kafka.apache.org/quickstart). 
```buildoutcfg
> bin/zookeeper-server-start.sh config/zookeeper.properties
> bin/kafka-server-start.sh config/server.properties
```


## 3. Build Kafka Topics

**NOTE:** A configuration file **must** be set before we start building Kafka topics.
The configuration file is ```config/producer.ini```. 

For basic setting, the following arguments should be proper:
* Kafka installation path
* topic names (for listening from Streaming API or archive files)
* For Streaming API: API secret key and tokens
* For Archive files: the location of archive folder; the starting Unix time and the ending Unix time

Now we can first build the raw tweets topic by running:
```commandline
python3 Runs/build_topic.py -s [stream or archive]
```
Then we can build a preprocessed tweets topic for further running by:
```commandline
python3 Runs/build_preprocessed_topic.py -s [stream or archive]
```
There are other options for preprocessing the tweets, including:
* *--crawl-url/--no-crawl-url*: indicating whether or not crawl the web page titles in each tweet. (default: no)
* *--keep-hashtag/--no-keep-hashtag*: indicating whether or not keeping the hashtag words in cleaned text. (default: keep)
* *--keep-url/--no-keep-url*: indicating whether or not keeping the url words in cleaned text. (default: no)
* *--keep-stopword/no-keep-stopword*: indicating whether or not keeping stop words in cleaned text. (default: no)
* *--ascii-filter/--no-ascii-filter*: indicating whether or not using ASCII filter to remove non-ASCII characters from the cleaned text. (default: use)
* *--ascii-count*: indicating the minimum number of ASCII character tokens after cleaning the text for detecting junk tweets. (default: 3)
* *--hashtag-count*: indicating the maximum number of hashtag tokens in a tweet for junk tweet detection. (default: 5)

**WARNING:** The crawling could be very slow and for many web pages, we might not be able to correctly fetch their page titles.

**NOTE:** We can start the preprocessed topic for Streaming API right after we start the raw tweets topic. 
However, for archive files, we should wait util seeing the logging information of "Start working on file XXX",
which means the system has finished decompressing the archive files and started producing to the raw tweets topic.

## 4. Runs
To build a run, we need to set up a configuration file for the runs in ```config/runs.ini```. Basically we need to set:
* the file path for TREC topic file (supports RTS16 and RTS17 style)
* *The connection to the broker*

A TREC style run output file could be built by running:

```commandline
python3 Runs/start_run.py -s [stream or archive] --no-crawl-url -o [output_path] -r [runname] -m [relevance measurement method] [-T [threshold]] -d [similarity method] [-U [similarity threshold]]
```
If you would like to add more relevance measurement methods or similarity measurement methods, you can put the scripts under folder
```Relevance``` or ```Similarity``` and modify the ```api.py``` module in them. 

[//]: # (System Overview Google Doc:)
[//]: # (https://docs.google.com/drawings/d/1cXnlvX4cQSX1yVulzVuHZX2xMGL_-y7AcHn7Ye9_uSI/edit?usp=sharing)

[//]: # (Kafka Documentation Google Doc:)
[//]: # (https://docs.google.com/document/d/1s4U9_PnZavxH_ryUaRa71rIB0OY6ixkkDpqPENsegIc/edit?usp=sharing)
