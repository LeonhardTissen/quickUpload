from flask import Flask
import waitress

app = Flask(__name__)
PORT = 5776
THREADS = 4

from routes import index, login, logout, dashboard, delete, create_user, upload, file, users

if __name__ == '__main__':
	waitress.serve(app, host='0.0.0.0', port=PORT, threads=THREADS)
