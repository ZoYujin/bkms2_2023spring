from pathlib import Path
from random import choice, choices
from datetime import datetime as dt
from datetime import timedelta
import psycopg

class DataGenerator():
    DATETIME_FMT = '%Y-%m-%dT%H:%M:%S'
    def __init__(self):
        with Path('names.txt').open('r') as file:
            self.names = [name.strip().lower() for name in file.readlines()]
            self.locations = list(range(5))

    def generate(self, timestamp: dt):
        name = choice(self.names)
        loc = choice(self.locations)
        return {
            'timestamp': timestamp.strftime(self.DATETIME_FMT), 
            'name': name,
            'location': loc,
        }

if __name__ == '__main__':
    with psycopg.connect(
        user="postgres",
        password="1234",
        host="localhost",
        port="5432"
    ) as conn:
        with conn.cursor() as cur:
            cur.execute("DROP TABLE IF EXISTS login;")
            cur.execute("""
                CREATE TABLE login (
                    lid INTEGER PRIMARY KEY NOT NULL,
                    ts VARCHAR(255),
                    name VARCHAR(255),
                    location INTEGER
                );
                """)
            
            generator = DataGenerator()
            timestamp = dt.now()
            n = 1000
            for i in range(1, n+1):
                random_wait_days = choices([0, 1, 3, 5, 10], weights=[0.80, 0.05, 0.05, 0.025, 0.025])[0]
                random_wait_hours = choice([0, 1])
                random_wait_minutes = choice([0, 10, 15, 20, 25])
                random_wait_seconds = choice([0, 1, 3, 5, 10])
                timestamp = timestamp + timedelta(
                    days=random_wait_days, 
                    hours=random_wait_hours, 
                    minutes=random_wait_minutes, 
                    seconds=random_wait_seconds
                )
                data = generator.generate(timestamp)
                cur.execute(
                    "INSERT INTO login(lid, ts, name, location) VALUES (%s, %s, %s, %s)", 
                    (i, data['timestamp'], data['name'], data['location'])
                )
            
            cur.execute("SELECT * FROM login LIMIT 5;")
            print('Check:')
            for a in cur.fetchall():
                print(a)