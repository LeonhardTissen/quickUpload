from __main__ import app
from flask import make_response, redirect, request

@app.route('/logout')
def logout():
	response = make_response(redirect('/login'))
	response.delete_cookie('username')
	response.delete_cookie('password')
	print(f'{request.cookies.get("username")} logged out')
	return response
