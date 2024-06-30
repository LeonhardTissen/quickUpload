from __main__ import app
from flask import request, redirect
from utils.user import get_user

@app.route('/', methods=['GET'])
def index():
	user = get_user(request)

	if user:
		return redirect('/dashboard')

	return redirect('/login')
	
