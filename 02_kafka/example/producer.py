# https://docs.confluent.io/platform/current/clients/confluent-kafka-python/html/index.html
from confluent_kafka  import Producer
from argparse import ArgumentParser, FileType
from configparser import ConfigParser
from random import choice
from datetime import datetime as dt
import time

if __name__ == '__main__':
    # Parse the command line.
    parser = ArgumentParser()
    parser.add_argument('config_file', type=FileType('r'))
    args = parser.parse_args()

    # Parse the configuration.
    # See https://github.com/edenhill/librdkafka/blob/master/CONFIGURATION.md
    config_parser = ConfigParser()
    config_parser.read_file(args.config_file)
    config = dict(config_parser['default'])

    producer = Producer(config)
    DATETIME_FMT = '%Y-%m-%d''T''%H:%M:%S'
    def delivery_callback(err, msg):
        if err:
            print('ERROR: Message failed delivery: {}'.format(err))
        else:
            utc_time = msg.timestamp()[1]
            if utc_time > 1e10:
                utc_time /= 1e3
            print("[{t}] topic {topic}: offset = {offset} key = {key:12} value = {value:12}".format(
                    t=dt.utcfromtimestamp(utc_time).strftime(DATETIME_FMT), 
                    offset=msg.offset(),
                    topic=msg.topic(), 
                    key=msg.key().decode('utf-8'), 
                    value=msg.value().decode('utf-8')
                ))

    # Produce data by selecting random values from these lists.
    topic = "purchases"
    user_ids = ['eabara', 'jsmith', 'sgarcia', 'jbernard', 'htanaka', 'awalther']
    products = ['book', 'alarm clock', 't-shirts', 'gift card', 'batteries']
    try:
        while True:
            random_wait = choice([1, 2, 3])
            time.sleep(random_wait)
            user_id = choice(user_ids)
            product = choice(products)
            producer.produce(
                topic=topic, 
                value=product, 
                key=user_id, 
                timestamp=int(dt.utcnow().timestamp()),
                callback=delivery_callback
            )
            producer.poll(100)
    except KeyboardInterrupt:
        pass
    finally:
        # Leave group and commit final offsets
        producer.flush()