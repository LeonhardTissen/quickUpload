from __main__ import app
from flask import send_from_directory

@app.route('/<username>/<filename>')
def file(username, filename):
	return send_from_directory(f'uploads/{username}', filename)
