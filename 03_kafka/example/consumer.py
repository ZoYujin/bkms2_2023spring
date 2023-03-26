from confluent_kafka import Consumer, OFFSET_BEGINNING
from argparse import ArgumentParser, FileType
from configparser import ConfigParser
from datetime import datetime as dt
import pandas as pd

if __name__ == '__main__':
    # Parse the command line.
    parser = ArgumentParser()
    parser.add_argument('config_file', type=FileType('r'))
    parser.add_argument('--reset', action='store_true')
    args = parser.parse_args()

    # Parse the configuration.
    # See https://github.com/edenhill/librdkafka/blob/master/CONFIGURATION.md
    config_parser = ConfigParser()
    config_parser.read_file(args.config_file)
    config = dict(config_parser['default'])
    config.update(config_parser['consumer'])

    # Create Consumer instance
    consumer = Consumer(config)

    # Set up a callback to handle the '--reset' flag.
    def reset_offset(consumer, partitions):
        if args.reset:
            for p in partitions:
                p.offset = OFFSET_BEGINNING
            consumer.assign(partitions)

    # Subscribe to topic
    topic = "purchases"
    consumer.subscribe([topic], on_assign=reset_offset)
    DATETIME_FMT = '%Y-%m-%d''T''%H:%M:%S'
    # Poll for new messages from Kafka and print them.
    data = {'name': [], 'itmes': []}
    try:
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                # Initial message consumption may take up to
                # `session.timeout.ms` for the consumer group to
                # rebalance and start consuming
                print("Waiting...")
            elif msg.error():
                print("ERROR: %s".format(msg.error()))
            else:
                # Extract the (optional) key and value, and print.
                utc_time = msg.timestamp()[1]
                if utc_time > 1e10:
                    utc_time /= 1e3
                print("[{t}] topic {topic}: offset = {offset} key = {key:10} value = {value:12}".format(
                        t=dt.utcfromtimestamp(utc_time).strftime(DATETIME_FMT), 
                        offset=msg.offset(),
                        topic=msg.topic(), 
                        key=msg.key().decode('utf-8'), 
                        value=msg.value().decode('utf-8')
                    ))
                    # create a monitoring dictionary
                data['name'].append(msg.key().decode('utf-8'))
                data['itmes'].append(msg.value().decode('utf-8'))
                
                if msg.offset() % 10 == 0:
                    # create a dataframe from the dictionary
                    df = pd.DataFrame(data).groupby('name').count()
                    print(df)

    except KeyboardInterrupt:
        pass
    finally:
        # Leave group and commit final offsets
        consumer.close()