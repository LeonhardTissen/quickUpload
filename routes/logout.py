from __main__ import app
from flask import make_response, redirect

@app.route('/logout')
def logout():
	response = make_response(redirect('/login'))
	response.delete_cookie('username')
	response.delete_cookie('password')
	return response
