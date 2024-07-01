import sqlite3
import os

class Database:
    def __init__(self):
        self.db_name = 'users.db'
        
        if not os.path.exists(self.db_name):
            self.create_table()
            username = input('Enter admin username: ')
            password = input('Enter admin password: ')
            self.add_user(username, password, 1)

    def create_table(self):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute('''
            CREATE TABLE users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                password TEXT,
                admin INTEGER
            )
        ''')
        conn.commit()
        conn.close()
        print('created table users')

    def clean_username(self, username):
        username = username.strip().lower()
        return ''.join([c for c in username if c.isalnum()])

    def add_user(self, username, password, admin=0):
        username = self.clean_username(username)
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        try:
            c.execute('INSERT INTO users VALUES (?, ?, ?, ?)', (None, username, password, admin))
            conn.commit()
        except sqlite3.IntegrityError:
            raise sqlite3.IntegrityError
        conn.close()
        print(f'added user {username}')

    def get_users(self):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute('SELECT id, username, password, admin FROM users')
        users = c.fetchall()
        conn.close()
        return {username: {
            'id': id,
            'username': username,
            'password': password,
            'admin': admin
        } for id, username, password, admin in users}

    def get_user(self, username):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute('SELECT id, username, password, admin FROM users WHERE username=?', (username,))
        user = c.fetchone()
        conn.close()
        if user:
            id, username, password, admin = user
            return {
                'id': id,
                'username': username,
                'password': password,
                'admin': admin
            }
        return None

db = Database()
