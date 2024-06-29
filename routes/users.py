from __main__ import app
from flask import render_template, request, redirect
from db import get_users

@app.route('/users')
def users():
	users = get_users()

	cookies = request.cookies

	if 'username' in cookies:
		username = cookies['username']
		if username in users:
			user = users[username]
			if user['password'] == cookies['password'] and user['admin'] == 1:
				users_list = []
				for user in users:
					users_list.append({
						'username': user,
						'admin': users[user]['admin'],
						'id': users[user]['id']
					})
				username = cookies['username']
				id = users[username]['id']
				return render_template('users.html.j2', users=users_list, username=username, id=id)

	return redirect('/')
