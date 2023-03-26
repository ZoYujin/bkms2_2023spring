# ksqlDB

Exercise on ksqlDB.

First run docker machines:

```shell
docker-compose up -d
```

Check machine status

```
docker ps
```

## Run ksqlDB in docker

```shell
docker exec -it ksqldb-cli ksql http://ksqldb-server:8088
```

## Create Stream

create stream

```sql
CREATE STREAM movements (person VARCHAR KEY, location VARCHAR) 
WITH (VALUE_FORMAT='JSON', PARTITIONS=1, KAFKA_TOPIC='movements');
```

show current streams

```sql
show streams;
```

insert stream values

```sql
INSERT INTO movements VALUES ('Allison', 'Denver');
INSERT INTO movements VALUES ('Robin', 'Leeds');
INSERT INTO movements VALUES ('Robin', 'Ilkley');
INSERT INTO movements VALUES ('Allison', 'Boulder');
```

## Query Data

offset setting

```sql
SET 'auto.offset.reset' = 'earliest';
-- use UNSET to revert
```

select data from the stream

```sql
SELECT * FROM MOVEMENTS EMIT CHANGES;
```

## Create table

```sql
CREATE TABLE person_stats WITH (VALUE_FORMAT='AVRO') AS
  SELECT person,
    LATEST_BY_OFFSET(location) AS latest_location,
    COUNT(*) AS location_changes,
    COUNT_DISTINCT(location) AS unique_location
  FROM movements
  GROUP BY person
EMIT CHANGES;
```

## REST API

You can use `curl` to run ksql with REST API

* for windows powershell

  ```
  -H > -contenttype
  -X > -method
  --data > -body
  -s > -uri
  ```

```bash
curl -X "POST" "http://localhost:8088/ksql" \
  -H "Accept: application/vnd.ksql.v1+json" \
  -d $'{
    "ksql": "show tables;",
    "streamsProperties": {}
  }'
```

```bash
curl -s -o response.txt -X "POST" "http://localhost:8088/query" \
  -H "Accept: application/vnd.ksql.v1+json" \
  -d $'{
    "ksql": "SELECT * FROM PERSON_STATS WHERE person =\'Allison\';",
    "streamsProperties": {}
  }'
```

## Connect with RDBMS

references: https://docs.ksqldb.io/en/0.10.2-ksqldb/tutorials/embedded-connect/

after run your machine, lets insert some data using python

```shell
python generate.py
```

and run ksqlDB CLI

```shell
docker exec -it ksqldb-cli ksql http://ksqldb-server:8088
```

before you issue more commands, tell ksqlDB to start all queries from earliest point in each topic:

```sql
SET 'auto.offset.reset' = 'earliest';
```

create connector with JDBC Connector

```
CREATE SOURCE CONNECTOR jdbc_login_reader WITH (
  'connector.class'          = 'io.confluent.connect.jdbc.JdbcSourceConnector',
  'connection.url'           = 'jdbc:postgresql://postgresql:5432/postgres',
  'connection.user'          = 'postgres',
  'connection.password'      = '1234',
  'topic.prefix'             = 'jdbc_',
  'table.whitelist'          = 'login',
  'mode'                     = 'incrementing',
  'numeric.mapping'          = 'best_fit',
  'incrementing.column.name' = 'lid',
  'key'                      = 'lid',
  'key.converter'            = 'org.apache.kafka.connect.converters.IntegerConverter');
```

```sql
SHOW CONNECTORS;
```

```sql
SHOW TOPICS;
```

Table Info: login
- `lid`: `INTEGER PRIMARY`
- `ts`: `VARCHAR(255)`
- `name`: `VARCHAR(255)`
- `location`: `INTEGER`

create stream

```sql
CREATE STREAM logins
WITH (
  kafka_topic = 'jdbc_login', 
  value_format = 'avro', 
  timestamp = 'ts', 
  timestamp_format = 'yyyy-MM-dd''T''HH:mm:ss'
);
```

see documentation to run some queries: https://docs.ksqldb.io/en/latest/developer-guide/ksqldb-reference/

Select the stream data where login location is 1 

```sql
SELECT ts, name, location 
FROM logins
WHERE location = 1
LIMIT 5;
```

Select the stream data in Sep. and Oct.

```sql
SELECT * FROM logins
WHERE ts >= '2022-09-01T00:00:00'
  AND ts <= '2022-10-31T23:59:59'
EMIT CHANGES;
```

https://docs.ksqldb.io/en/latest/concepts/time-and-windows-in-ksqldb-queries/

process by window: see how many people login at each location for each 15 days  

```sql
SELECT 
  FORMAT_TIMESTAMP(FROM_UNIXTIME(windowstart), 'yyyy-MM-dd') AS win_start, 
  FORMAT_TIMESTAMP(FROM_UNIXTIME(windowend), 'yyyy-MM-dd') AS win_end,
  location, COUNT_DISTINCT(name)
FROM logins
WINDOW TUMBLING (SIZE 15 DAY)
GROUP BY location
EMIT CHANGES;
```

delete stream with topic

```sql
DROP STREAM logins DELETE TOPIC
```