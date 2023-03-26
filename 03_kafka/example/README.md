# Kafka CLI

Go to kafak directory

```bash
$ cd kafka_2.13-2.8.1
```

## Run Zookeeper

* We'll use Linux/Mac OS as default setting

```bash
# Linux/Mac OS
$ bin/zookeeper-server-start.sh config/zookeeper.properties

# Windows
$ bin/windows/zookeeper-server-start.bat config/zookeeper.properties
```

## Run Kafka Server

modify `server.properties`

```bash
$ vi config/server.properties
```

```
dataDir=/tmp/zookeeper
clientPort=2181
maxClientCnxns=0
admin.enableServer=false
```

start kafka server

```bash
$ bin/zookeeper-server-start.sh config/zookeeper.properties
```

## Create and Check Topics

```bash
# create topics
$ bin/kafka-topics.sh --bootstrap-server localhost:9092 --topic test --create 
# create topics with 3 partitions
$ bin/kafka-topics.sh --bootstrap-server localhost:9092 --partitions 3 --topic test2 --create 

# check topics
$ bin/kafka-topics.sh --bootstrap-server localhost:9092 --topic test --describe

# list all topics 
$ bin/kafka-topics.sh --bootstrap-server localhost:9092 --list
```

## Producer

```bash
# producer without keys
$ bin/kafka-console-producer.sh --bootstrap-server localhost:9092 --topic test

# check logs
$ cat data/test-0/00000000000000000000.log

# producer with keys
$ bin/kafka-console-producer.sh --bootstrap-server localhost:9092 \
    --topic test2 \
    --property "parse.key=true" \
    --property "key.separator=:"
```

## Consumer

```bash
# consume data from topic test
$ bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic test --from-beginning

# consume data from topic test2
$ bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 \
    --topic test2 --from-beginning \
    --property print.key=true --property key.separator="-" 

# consume data from topic test2 in partition 2
$ bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 \
    --topic test2 --from-beginning --partition 2 \
    --property print.key=true --property key.separator="-"

# consume data by group
$ bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 \
    --topic test --group test-group --from-beginning 
```

## Consumer Group

```bash
# list consumed group
$ bin/kafka-consumer-groups.sh --bootstrap-server localhost:9092 --list

# check before/after run 'kafka-console-producer.sh' with group 
# CURRENT-OFFSET, LOG-END-OFFSET, LAG
$ bin/kafka-consumer-groups.sh --bootstrap-server localhost:9092 --group test-group --describe

# check before/after run 'kafka-console-producer.sh' with group
$ bin/kafka-consumer-groups.sh --bootstrap-server localhost:9092 \
    --group test-group --topic test \
    --reset-offsets --to-earliest --execute
```

## Remove the program

```bash
# remove data folder
$ rm -rf ./data

# remove zookeeper logs
# for windows delete C:/tmp/zookeeper
$ rm -rf /tmp/zookeeper
```

---

# Confluentic.io Kafka Python API

```bash
# go to folder example
$ cd example

# turn on the docker machine
# d: detach mode / f: docker-compose file
$ docker-compose -f docker-compose.yml up -d
```

## Start Producer

```bash
$ python producer.py config.ini
```

## Start Consumer

```bash
$ python consumer.py config.ini
```

## Check consumed data

```bash
# attach into kafak machine
$ docker-compose exec kafka1 bash

# check the topic consumed
$ kafka-consumer-groups --bootstrap-server 0.0.0.0:9092 \
    --group purchase-group --describe
```