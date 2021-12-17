import sqlite3
import datetime
import random
con = sqlite3.connect('database.db')

cur = con.cursor()

users = []

for row in cur.execute("SELECT * FROM users where name != 'dots'"):
    users.append((row[0], row[3]))

#for user in users:
#    cur.execute("INSERT INTO transactions (created_at, source_user_id, destination_user_id, amount) VALUES (?, ?, ?, ?)", (datetime.datetime(2021, 1, 1, 0, 0, 0), 'dots', user[0], 100000))

balances = {}
curr_date = datetime.datetime(2021, 1, 1, 0, 0, 0)

for user in users:
    balances[user[0]] = 100000

for i in range(50):
    source_user = random.choice(users)
    source_user_id = source_user[0]
    destination_user = random.choice(users)
    destination_user_id = destination_user[0]
    while source_user_id == destination_user_id:
        destination_user = random.choice(users)
        destination_user_id = destination_user[0]
    
    curr_date += datetime.timedelta(days=random.randint(1, 7))

    balance = balances[source_user_id]

    if balance > 0:
        amount_to_transfer = random.randint(100, min(10000, balance))
        balances[source_user_id] -= amount_to_transfer
        balances[destination_user_id] += amount_to_transfer
        cur.execute("INSERT INTO transactions (created_at, source_user_id, destination_user_id, amount) VALUES (?, ?, ?, ?)", (curr_date, source_user_id, destination_user_id, amount_to_transfer))
    

con.commit()
