from __main__ import app
from flask import request, redirect
import os
from utils.user import get_user

def is_valid_character(c):
	return c.isalnum() or c == '.'

def clean_filename(filename):
	only_alphanumeric = ''.join(c for c in filename if is_valid_character(c)).strip()

	file_name = ''.join(only_alphanumeric.split('.')[0])
	file_ext = only_alphanumeric.replace(file_name, '')
	length_trimmed = file_name[:32] + file_ext

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
		return 'Invalid user', 401
	
	username = user['username']
	
	files = request.files.getlist('file')
	if len(files) == 0:
		return 'No files uploaded', 400

	directory = f'uploads/{username}'
	os.makedirs(directory, exist_ok=True)

	for file in files:
		if file.filename == '':
			continue

		filename = clean_filename(file.filename)
		location = f'{directory}/{filename}'

		while os.path.exists(location):
			filename = add_number(filename)
			location = f'{directory}/{filename}'
		
		file.save(location)
		print(f'{username} uploaded {location}')

	return 'Files uploaded successfully', 200

@app.route('/combine', methods=['POST'])
def combine():
	user = get_user(request)

	if not user:
		return 'Invalid user', 401
	
	username = user['username']
	directory = f'uploads/{username}'

	large_file_parts = {}

	files = os.listdir(directory)

	for file in files:
		if '.part' not in file:
			continue

		file_name = file.split('.part')[0]
		part_number = int(file.split('.part')[1])
		if file_name not in large_file_parts:
			large_file_parts[file_name] = {}
		large_file_parts[file_name][part_number] = file

	for file_name, parts in large_file_parts.items():
		combined_filename = clean_filename(file_name)
		combined_location = f'{directory}/{combined_filename}'
		
		while os.path.exists(combined_location):
			combined_filename = add_number(combined_filename)
			combined_location = f'{directory}/{combined_filename}'
		
		with open(combined_location, 'wb') as combined_file:
			for part_number in sorted(parts.keys()):
				part_file = parts[part_number]
				part_location = f'{directory}/{part_file}'
				with open(part_location, 'rb') as part_file_obj:
					combined_file.write(part_file_obj.read())
				os.remove(part_location)
		print(f'{username} combined and saved {combined_location}')

	return 'Files combined successfully', 200
