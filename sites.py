from flask import Flask, render_template, request, make_response, redirect, send_from_directory
import os
from db import add_user, get_users

app = Flask(__name__)

PORT = 5776

@app.route('/', methods=['GET', 'POST'])
def index():
	users = get_users()
	print(users)
	
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']

		if username in users:
			user = users[username]
			if user['password'] == password:
				response = make_response(render_template('redirect.html.j2', username=username))
				response.set_cookie('username', username)
				response.set_cookie('password', password)
				return response

		return render_template('login.html.j2', message='Invalid username or password')
	
	cookies = request.cookies

	if 'username' in cookies:
		username = cookies['username']
		if username in users:
			user = users[username]
			if user['password'] == cookies['password']:
				return redirect('/dashboard')
	
	return render_template('login.html.j2')

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
				print(username, files, admin)
				return render_template('dashboard.html.j2', username=username, id=id, files=files, admin=admin)

	return redirect('/')

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

@app.route('/logout')
def logout():
	response = make_response(redirect('/'))
	response.delete_cookie('username')
	response.delete_cookie('password')
	return response

@app.route('/create_user', methods=['POST'])
def create_user():
	users = get_users()

	cookies = request.cookies

	if 'username' in cookies:
		username = cookies['username']
		if username in users:
			user = users[username]
			# Allow admin to create new users
			if user['password'] == cookies['password'] and user['admin'] == 1:
				new_username = request.form['username']
				new_password = request.form['password']
				try:
					add_user(new_username, new_password)
					return render_template('redirect.html.j2', message='User created')
				except:
					return render_template('redirect.html.j2', message='User already exists')
					

	return redirect('/')

@app.route('/<username>/<filename>')
def download(username, filename):
	return send_from_directory(f'uploads/{username}', filename)

if __name__ == '__main__':
	app.run(debug=True, port=PORT)
