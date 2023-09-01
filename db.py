import utils

def connect_to_database(name='database.db'):
	import sqlite3
	return sqlite3.connect(name, check_same_thread=False)

def init_db(connection):
	cursor = connection.cursor()

	cursor.execute('''
		CREATE TABLE IF NOT EXISTS users (
			id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
			username TEXT NOT NULL UNIQUE,
			password TEXT NOT NULL
		)
	''')

	connection.commit()


def add_user(connection,first_name,last_name,email, username, password):
    cursor = connection.cursor()
    hashed_password = utils.hash_password(password)
    query = '''INSERT INTO users (first_name,last_name,email, username, password) VALUES (?,?,?,?, ?)'''
    cursor.execute(query, (first_name,last_name,email,username, hashed_password))
    connection.commit()

def get_user(connection, email, username):
    cursor = connection.cursor()
    query = '''SELECT * FROM users WHERE email = ? OR username =?'''
    cursor.execute(query, (email, username))
    return cursor.fetchone()


def get_all_users(connection):
	cursor = connection.cursor()
	query = 'SELECT * FROM users'
	cursor.execute(query)
	return cursor.fetchall()