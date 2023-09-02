import utils


def seed_admin_user(username,password):
    admin_username = 'admin'
    admin_password = 'admin1234'

    if username==admin_username and password==admin_password:
        return True
    return False
         
         
    

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




def init_restaurant(connection):
    cursor = connection.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS restaurants (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL UNIQUE,
            description TEXT,
            image_url TEXT
           
        )
    ''')

    connection.commit()
    
    

def add_restaurant(connection, title, description, image_url=None):
    cursor = connection.cursor()
    query = '''INSERT INTO restaurants ( title, description, image_url) VALUES (?, ?, ?)'''
    cursor.execute(query, ( title, description, image_url))
    connection.commit()

def get_restaurant(connection, restaurant_id):
    cursor = connection.cursor()
    query = '''SELECT * FROM restaurants WHERE id = ?'''
    cursor.execute(query, (restaurant_id,))
    return cursor.fetchone()


def get_all_restaurants(connection):
    cursor = connection.cursor()
    query = '''SELECT * FROM restaurants'''
    cursor.execute(query)
    return cursor.fetchall()

def init_comments_table(connection):
    cursor = connection.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS comments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            restaurant_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            text TEXT NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (restaurant_id) REFERENCES restaurants (id),
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')

    connection.commit()
    

def add_comment(connection, restaurant_id, user_id, text):
    cursor = connection.cursor()
    query = '''INSERT INTO comments (restaurant_id, user_id, text) VALUES (?, ?, ?)'''
    cursor.execute(query, (restaurant_id, user_id, text))
    connection.commit()

def get_comments_for_restaurant(connection, restaurant_id):
    cursor = connection.cursor()
    query = '''
        SELECT  users.username, comments.text, comments.timestamp
        FROM comments
        JOIN users ON comments.user_id = users.id
        WHERE comments.restaurant_id = ?
    '''
    cursor.execute(query, (restaurant_id,))
    return cursor.fetchall()