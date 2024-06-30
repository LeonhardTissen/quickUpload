from flask import Flask
import sys

app = Flask(__name__)
HOST = '0.0.0.0'
PORT = 5776
THREADS = 4
DEBUG = sys.argv[1] == 'debug' if len(sys.argv) > 1 else False

from routes import index, login, logout, dashboard, delete, create_user, upload, file, users

if __name__ == '__main__':
	if DEBUG:
		app.run(host=HOST, port=PORT, debug=True)
	else:
		import waitress
		waitress.serve(app, host=HOST, port=PORT, threads=THREADS)
