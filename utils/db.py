import sqlite3
import os

def create_table():
	conn = sqlite3.connect('users.db')
	c = conn.cursor()
	c.execute('CREATE TABLE users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE, password TEXT, admin INTEGER)')
	conn.commit()
	conn.close()

def clean_username(username):
	username = username.strip().lower()
	return ''.join([c for c in username if c.isalnum()])

def add_user(username, password, admin=0):
	username = clean_username(username)
	
	conn = sqlite3.connect('users.db')
	c = conn.cursor()
	try:
		c.execute('INSERT INTO users VALUES (?, ?, ?, ?)', (None, username, password, admin))
		conn.commit()
	except sqlite3.IntegrityError:
		raise sqlite3.IntegrityError
	conn.close()

def get_users():
	conn = sqlite3.connect('users.db')
	c = conn.cursor()
	c.execute('SELECT * FROM users')
	users = c.fetchall()
	conn.close()
	return {username: {
		'id': id,
		'username': username,
		'password': password,
		'admin': admin
	} for id, username, password, admin in users}

def init():
	if not os.path.exists('users.db'):
		create_table()
		admin = input('Enter admin username: ')
		password = input('Enter admin password: ')
		add_user(admin, password, 1)

init()
