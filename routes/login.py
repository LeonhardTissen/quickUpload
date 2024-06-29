from __main__ import app
from flask import request, render_template, make_response
from db import get_users

@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'GET':
		return render_template('login.html.j2')
	
	users = get_users()

	username = request.form['username']
	password = request.form['password']

	if username in users:
		user = users[username]
		if user['password'] == password:
			response = make_response(render_template('redirect.html.j2', username=username))
			response.set_cookie('username', username)
			response.set_cookie('password', password)
			return response

	return render_template('login.html.j2', message='Invalid username or password')
