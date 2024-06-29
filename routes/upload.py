from __main__ import app
from flask import request, redirect
from db import get_users
import os

@app.route('/upload', methods=['POST'])
def upload():
	users = get_users()

	cookies = request.cookies

	if 'username' in cookies:
		username = cookies['username']
		if username in users:
			user = users[username]
			if user['password'] == cookies['password']:
				files = request.files.getlist('file')
				if len(files) == 0:
					return redirect('/dashboard')
				
				for file in files:
					if file.filename == '':
						continue
					
					cleaned_filename = file.filename.replace(' ', '_')
					directory = f'uploads/{username}'
					os.makedirs(directory, exist_ok=True)
					location = f'{directory}/{cleaned_filename}'
					file.save(location)
				
				return redirect('/dashboard')

	return redirect('/')
