import sys
import socket
from util.messages import Error, Success

# collect login arguments
def fetch_args(argv):
	if len(argv) != 4:
		print(Error.wrong_param)
		sys.exit()
	ip, port, username = get_ip(argv), get_port(argv), get_username(argv)
	return ip, port, username

# check and return server IP address
# helper function for fetch_args()
def get_ip(argv):
	ip = argv[1]
	try:
		socket.inet_aton(ip)
	except:
		print(Error.invalid_ip)
		sys.exit()
	return ip

# check and return server port number
# helper function for fetch_args()
def get_port(argv):
	port = argv[2]
	try:
		port = int(port)
		if port < 1024 or port > 65535:
			raise Exception('invalid range')
	except:
		print(Error.invalid_port)
		sys.exit()
	return port

# check and return username
# helper function for fetch_args()
def get_username(argv):
	username = argv[3]
	if not username.isalnum():
		print(Error.invalid_username)
	return username


# Below are related and useful links
# ip and port range: https://piazza.com/class/k530q3x9ywp55n?cid=341
# client output sample: https://drive.google.com/drive/u/1/folders/1ZtjS9nE9Q0SLrj0K25o_J5zGV9211Ykf