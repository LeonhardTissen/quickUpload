from flask import Flask
from flask_minify import Minify

import sys

app = Flask(__name__)
Minify(app=app, html=True, js=True, cssless=True)
HOST = '0.0.0.0'
PORT = 5776
THREADS = 4
DEBUG = sys.argv[1] == 'debug' if len(sys.argv) > 1 else False

from routes import index, login, logout, dashboard, delete, create_user, upload, file, users
from utils import beforerequest

if __name__ == '__main__':
	if DEBUG:
		app.run(host=HOST, port=PORT, debug=True)
	else:
		import waitress
		waitress.serve(app, host=HOST, port=PORT, threads=THREADS)
