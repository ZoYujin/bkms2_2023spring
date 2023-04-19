# Assignment 3

> Due: 2023-04-25 23:59

- Please upload a single pdf file.
- If you submit assignments after the due date, each day will decrease by 10% from the score. e.g., Submit before 2023-04-26 23:59: -10%

Please Make sure your code is executable. To start the docker-machines please run:

```bash
$ cd 02_kafka/assignment
$ docker-compose up -d
```

## Objective

* Understand how does a Kafka cluster working in docker machines.
* Ability to run a Kafka cluster and ksqlDB-CLI with docker
* Understand how to connect other source applications to ksqlDB / Kafka cluster.
* Learn how to write ksql query with new statements(e.g., `WINDOW`, `EMIT CHANGES`, ...)

## Fraud Detection

<img src="./bitcoin.jpg" width="40%">

You are a data scientist in a financial card company. Some users try to hack the system to spend a lot of money, which is unreasonable. It would be best if you detected these abnormalities. So, you tried to build a simulation system to run some experiments. All the data will be generated from a python code(`producer.py`) and inserted into the PostgreSQL database. Information about table `transactions` is as follows: 

| Column Name | Type | Description |
|:--:|---| --- |
| tid | INTEGER PRIMARY KEY NOT NULL | Index of Table |
| ts | VARCHAR(30) | Timestamp that a user use the card |
| email_address | VARCHAR(100) | Email address, composed of 'user name' + '@card.com' |
| card_number | VARCHAR(20) | Card number, a user can have multiple cards |
| amount | NUMERIC(20, 2) | Amout of usage |

Please do following instruction and write your code for each question:

1. Run producer application `producer.py`(do not stop it).
2. Create a source connector called `transaction_reader` using `JdbcSourceConnector`. The producer will send every 10 data into the Kafka cluster. Check it with `PRINT [topic_name] FROM BEGINNING;`.
3. Create a stream called `transactions` with the proper topic name.
4. Write a monitoring query. You need to keep tracking if the summation of the `amount` on someone's card is larger than a threshold(=1000000000) for every day. Please refer `WINDOW` statement in [ksql documentation](https://docs.ksqldb.io/en/latest/developer-guide/ksqldb-reference/select-pull-query/#window). You have to give the following column names in the table: 
    * `win_start`: The window start with 'yyyy-MM-dd' format
    * `win_end`: The window end with 'yyyy-MM-dd' format
    * `last_trial_time`: The last timestamp the user uses the card between the window(=1 day). The format is 'yyyy-MM-dd''T''HH:mm:ss'.
    * `name`: User name extracted from `email_address` 
    * `card_number`: Card number
    * `sum_amount`: Summation of `amount`
5. Create a table called `sum_all_amount` group by user name. You have to give the following column names in the table: 
    * `name`: User name extracted from `email_address` 
    * `count`: Number of card usage for each user.
    * `sum_amount`: Summation of `amount`
6. From the result of `sum_all_amount` table or `transactions` stream, (1) Is the threshold(current = 1000000000) reasonable for monitoring the abnormalities? (2) How about monitoring window size(current = 1day)? Please describe your thought and why.

---

Useful documents:

- Useful usecases in confluent.io: [https://developer.confluent.io/tutorials/](https://developer.confluent.io/tutorials/)
- Create connectors: [https://docs.ksqldb.io/en/latest/developer-guide/ksqldb-reference/create-connector/](https://docs.ksqldb.io/en/latest/developer-guide/ksqldb-reference/create-connector/)
