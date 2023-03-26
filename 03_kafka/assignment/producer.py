from pathlib import Path
from random import choice, choices, randint, random
from datetime import datetime as dt
from datetime import timedelta
import time
import psycopg

class DataGenerator():
    DATETIME_FMT = '%Y-%m-%dT%H:%M:%S'
    def __init__(self, abnormal_threshold: float=0.99):
        with Path('names.txt').open('r') as file:
            self.names = [name.strip().lower() for name in file.readlines()]
        # build customer information
        self.issued = set()
        self.names_dict = {}
        for n in self.names:
            info = {}
            info['danger'] = (abs(hash(n)) // 1e17) < 8
            n_card = choice([3, 4, 5]) if info['danger'] else choice([1, 2])
            info['cards'] = [self._issue_card_number() for _ in range(n_card)]
            self.names_dict[n] = info
        
        self.abnormal_threshold = abnormal_threshold
        self._reset_normal_cnt()

    def _issue_card_number(self):
        stop_issue = False
        if len(self.issued) >= 273435746624250:
            raise ValueError('Cannot issue a new card')
        while not stop_issue:
            card = '-'.join([str(randint(1000, 9999)) for _ in range(4)])
            if card not in self.issued:
                stop_issue = True
        self.issued.add(card)
        return card

    def _reset_normal_cnt(self):
        self._count = 0
        self._abnormal_count_thres = randint(100, 105)

    def _update_normal_cnt(self):
        self._count += 1
    
    def _check_abnormal_count_thres(self):
        if self._count == self._abnormal_count_thres:
            self._reset_normal_cnt()
            return True
        return False

    def generate_amount(self, name):
        if self.names_dict[name]['danger']:
            abnormal = choices([False, True], weights=[0.6, 0.4])[0]
        else:
            prob = random()
            abnormal = prob >= self.abnormal_threshold

        if self._check_abnormal_count_thres() or abnormal:
            self._reset_normal_cnt()
            return random() * 1e10
        else:
            self._update_normal_cnt()
            amount = random() * choices([10, 100, 1000, 1e4, 1e5], weights=[0.35, 0.4, 0.1, 0.1, 0.05])[0]
            if amount < 1:
                amount += 1
            return amount

    def generate(self, timestamp: dt):
        name = choice(self.names)
        email_address = name+'@card.com'
        card_number = choice(self.names_dict[name]['cards'])
        amount = self.generate_amount(name)
        return {
            'ts': timestamp.strftime(self.DATETIME_FMT), 
            'email_address': email_address,
            'card_number': card_number,
            'amount': round(amount, 2),
            'danger': self.names_dict[name]['danger']
        }

if __name__ == '__main__':
    generator = DataGenerator()
    timestamp = dt.now()
    i = 0
    with psycopg.connect(user="postgres", password="1234", host="localhost", port="5432") as conn:
        with conn.cursor() as cur:
            cur.execute("DROP TABLE IF EXISTS transactions;")
            cur.execute("""
                CREATE TABLE transactions (
                    tid INTEGER PRIMARY KEY NOT NULL,
                    ts VARCHAR(30),
                    email_address VARCHAR(100),
                    card_number VARCHAR(20),
                    amount NUMERIC(20, 2)
                );
                """)
    try:
        conn = psycopg.connect(user="postgres", password="1234", host="localhost", port="5432")
        while True:
            with conn.cursor() as cur:
                i += 1
                random_wait_days = choices([0, 1, 2], weights=[0.80, 0.1, 0.1])[0]
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
                time.sleep(0.5)
                cur.execute(
                    "INSERT INTO transactions(tid, ts, email_address, card_number, amount) VALUES (%s, %s, %s, %s, %s)", 
                    (i, data['ts'], data['email_address'], data['card_number'], data['amount'])
                )
                print('[{0}] Email: {1:18} | Card: {2} | Amount: ${3:20} | Is Fraud: {4}'.format(
                    data['ts'], data['email_address'], data['card_number'], data['amount'], data['danger']))
                if i % 10 == 0:
                    conn.commit()
    except KeyboardInterrupt:
        conn.commit()
        print('Keyboard Interrupted')
    finally:
        conn.close()
        print('Exit')