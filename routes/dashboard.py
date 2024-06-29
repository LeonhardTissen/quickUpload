from __main__ import app
from flask import request, render_template, redirect
from db import get_users
import os

@app.route('/dashboard')
def dashboard():
	users = get_users()

	cookies = request.cookies

	if 'username' in cookies:
		username = cookies['username']
		if username in users:
			user = users[username]
			if user['password'] == cookies['password']:
				admin = user['admin']
				id = user['id']
				os.makedirs(f'uploads/{username}', exist_ok=True)
				filelist = os.listdir(f'uploads/{username}')
				files = []
				for file in filelist:
					files.append({
						'filename': file,
						'url': f'/{username}/{file}'
					})
				return render_template('dashboard.html.j2', username=username, id=id, files=files, admin=admin)

	return redirect('/')
