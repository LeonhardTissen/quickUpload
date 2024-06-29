from __main__ import app
from flask import request, redirect
from db import get_users
import os

@app.route('/delete/<filename>', methods=['GET'])
def delete(filename):
	users = get_users()

	cookies = request.cookies

	if 'username' in cookies:
		username = cookies['username']
		if username in users:
			user = users[username]
			if user['password'] == cookies['password']:
				os.remove(f'uploads/{username}/{filename}')
				return redirect('/dashboard')

	return redirect('/')
