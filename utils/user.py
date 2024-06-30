from utils.db import db

def get_user(request):

	cookies = request.cookies

	# User is not logged in
	if not ('username' in cookies and 'password' in cookies):
		return None

	username = cookies['username']
	
	user = db.get_user(username)
	if not user:
		return None
	
	# Password is correct
	if user['password'] == cookies['password']:
		return user
	
	return None

def is_valid_user(request):
	return get_user(request) != None

def is_admin(request):
	user = get_user(request)
	
	if user:
		return user['admin'] == 1
	
	return False
