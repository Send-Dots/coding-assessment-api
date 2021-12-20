import requests
import datetime

def getBalance(username, date):
    
    response = requests.get("https://interview.senddots.com/users")
    users = response.json().get('users')

    user_id = None

    for user in users:
        if user['username'] == username:
            user_id = user['id']
            break
    
    transactions = requests.get("https://interview.senddots.com/transactions/" + str(user_id)).json().get('transactions')

    for transaction in transactions:
        transaction['date'] = datetime.datetime.strptime(transaction['date'], '%Y-%m-%d %H:%M:%S')

    balance = 0

    date = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')

    for transaction in transactions:
        if transaction['date'] <= date:
            if transaction['source_user_id'] == user_id:
                balance -= transaction['amount']
            elif transaction['destination_user_id'] == user_id:
                balance += transaction['amount']
    
    return balance

print(getBalance("dots", "2020-01-01 00:00:00"))