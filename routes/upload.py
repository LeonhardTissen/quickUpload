from __main__ import app
from flask import request, redirect
import os
from utils.user import get_user

def is_valid_character(c):
	return c.isalnum() or c == '.'

def clean_filename(filename):
	only_alphanumeric = ''.join(c for c in filename if is_valid_character(c)).strip()

	file_ext = only_alphanumeric.split('.')[-1]
	file_name = '.'.join(only_alphanumeric.split('.')[:-1])
	length_trimmed = file_name[:16] + '.' + file_ext

	return length_trimmed

def add_number(filename):
	file_ext = filename.split('.')[-1]
	file_name = filename.split('.')[0]
	if '_' in file_name:
		number = int(file_name.split('_')[-1]) + 1
		file_name = '_'.join(file_name.split('_')[:-1])
	else:
		number = 1
	return f'{file_name}_{number}.{file_ext}'

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
		
		filename = clean_filename(file.filename)
		directory = f'uploads/{username}'
		os.makedirs(directory, exist_ok=True)
		location = f'{directory}/{filename}'

		while os.path.exists(location):
			filename = add_number(filename)
			location = f'{directory}/{filename}'
			
		file.save(location)
		print(f'{username} uploaded {location}')
	
	return redirect('/dashboard')
