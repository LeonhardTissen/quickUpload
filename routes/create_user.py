from __main__ import app
from flask import request, render_template, redirect
from utils.db import add_user
from utils.user import is_valid_user, is_admin

@app.route('/create_user', methods=['POST'])
def create_user():
	if not (is_valid_user(request) and is_admin(request)):
		return redirect('/')
	
	new_username = request.form['username']
	new_password = request.form['password']
	try:
		add_user(new_username, new_password)
	except:
		return render_template('redirect.html.j2', message='User already exists', redirect='/users')
	
	return render_template('redirect.html.j2', message='User created', redirect='/users')
