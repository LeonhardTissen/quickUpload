from __main__ import app
from flask import render_template, request, redirect
from utils.user import get_user
from utils.db import db
import os

@app.route('/users')
def users():
	user = get_user(request)

	if not user or not user['admin']:
		return redirect('/')
	
	username, id = user['username'], user['id']

	users = db.get_users()
	
	users_list = []
	for user in users:
		user_obj = {
			'username': user,
			'admin': users[user]['admin'],
			'id': users[user]['id']
		}
		# Use du to get the size of the user's directory
		dir = os.getcwd()
		size = (os.popen(f'du -sh {dir}/uploads/{user}').read().split('\t')[0] or '0').lower() + 'b'
		user_obj['size'] = size 
		users_list.append(user_obj)
	print(f"{username} accessed the users page")
	return render_template('users.html.j2', users=users_list, username=username, id=id)
