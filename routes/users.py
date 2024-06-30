from __main__ import app
from flask import render_template, request, redirect
from utils.user import get_user
from utils.db import db

@app.route('/users')
def users():
	user = get_user(request)

	if not user or not user['admin']:
		return redirect('/')
	
	username, id = user['username'], user['id']

	users = db.get_users()
	
	users_list = []
	for user in users:
		users_list.append({
			'username': user,
			'admin': users[user]['admin'],
			'id': users[user]['id']
		})
	return render_template('users.html.j2', users=users_list, username=username, id=id)
