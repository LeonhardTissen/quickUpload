from __main__ import app
from flask import request, render_template, redirect
import os
from utils.db import get_users
from utils.user import get_user

@app.route('/dashboard')
def dashboard():
	user = get_user(request)

	if not user:
		redirect('/')

	username, admin, id = user['username'], user['admin'], user['id']
	os.makedirs(f'uploads/{username}', exist_ok=True)
	filelist = os.listdir(f'uploads/{username}')
	files = [{'filename': file, 'url': f'/{username}/{file}'} for file in filelist]
	return render_template('dashboard.html.j2', username=username, id=id, files=files, admin=admin)
