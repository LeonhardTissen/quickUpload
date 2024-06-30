from __main__ import app
from flask import request, redirect
import os
from utils.user import get_user

@app.route('/delete/<filename>', methods=['GET'])
def delete(filename):
	user = get_user(request)

	if not user:
		return redirect('/')

	username = user['username']
	path = f'uploads/{username}/{filename}'
	os.remove(path)
	print(f'{username} deleted {path}')
	return redirect('/dashboard')
