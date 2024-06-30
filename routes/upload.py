from __main__ import app
from flask import request, redirect
from utils.user import get_user
import os

@app.route('/upload', methods=['POST'])
def upload():
	user = get_user(request)

	if not user:
		return redirect('/')
	
	username = user['username']
	
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
