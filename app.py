import sqlite3

from flask import Flask
from flask import g
from flask import jsonify

DATABASE = 'database.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

app = Flask(__name__)

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route('/')
def test():
    return 'OK'


@app.route('/users', methods=['GET'])
def get_users():
    cur = get_db().cursor()
    users = cur.execute('SELECT * FROM users').fetchall()
    users = [{'id': user[0], 'name': user[2], 'username': user[3]} for user in users]
    return jsonify({'users': users}), 200


@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    cur = get_db().cursor()
    user = cur.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
    if user is None:
        return jsonify({'error': 'User not found'}), 404
    user = {'id': user[0], 'name': user[2], 'username': user[3]}
    return jsonify({'user': user}), 200


@app.route('/transactions/<int:user_id>', methods=['GET'])
def get_transactions(user_id):
    cur = get_db().cursor()
    transactions = cur.execute('SELECT * FROM transactions WHERE source_user_id = ? or destination_user_id = ?', (user_id, user_id)).fetchall()
    transactions = [{'id': transaction[0], 'date': transaction[1], 'source_user_id': transaction[2], 'destination_user_id': transaction[3], 'amount': transaction[4]} for transaction in transactions]
    return jsonify({'transactions': transactions}), 200


if __name__ == '__main__':
    app.run(debug=True)