from __main__ import app
from flask import request, render_template, redirect
from db import add_user, get_users

@app.route('/create_user', methods=['POST'])
def create_user():
	users = get_users()

	cookies = request.cookies

	if 'username' in cookies:
		username = cookies['username']
		if username in users:
			user = users[username]
			# Allow admin to create new users
			if user['password'] == cookies['password'] and user['admin'] == 1:
				new_username = request.form['username']
				new_password = request.form['password']
				try:
					add_user(new_username, new_password)
					return render_template('redirect.html.j2', message='User created')
				except:
					return render_template('redirect.html.j2', message='User already exists')
					

	return redirect('/')
