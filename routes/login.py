from __main__ import app
from flask import request, render_template, make_response
from utils.db import db

@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'GET':
		return render_template('login.html.j2')
	
	users = db.get_users()

	username = request.form['username']
	password = request.form['password']

	if not username in users:
		return render_template('login.html.j2', message='User does not exist')
	
	user = users[username]
	if user['password'] != password:
		return render_template('login.html.j2', message='Invalid username or password')
	
	response = make_response(render_template('redirect.html.j2', username=username, redirect='/dashboard'))
	response.set_cookie('username', username)
	response.set_cookie('password', password)
	return response

