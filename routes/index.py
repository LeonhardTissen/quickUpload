from __main__ import app
from flask import request, redirect
from db import get_users

@app.route('/', methods=['GET'])
def index():
	users = get_users()
	
	cookies = request.cookies

	if 'username' in cookies:
		username = cookies['username']
		if username in users:
			user = users[username]
			if user['password'] == cookies['password']:
				return redirect('/dashboard')
	
	return redirect('/login')
