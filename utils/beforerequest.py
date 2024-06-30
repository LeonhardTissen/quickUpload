from __main__ import app
from flask import request
from datetime import datetime

BLUE = '\033[94m'
CYAN = '\033[96m'
WHITE = '\033[0m'

@app.before_request
def beforerequest():
	addr = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
	time = datetime.now().strftime("[%H:%M:%S]")
	print(BLUE + time + ' ' + CYAN + "{:<16}".format(addr) + WHITE + request.url)
