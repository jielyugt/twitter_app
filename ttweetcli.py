import sys
import socket
from util.messages import Error, Success
import util.client_util
import shlex
import json
import threading
import re



def main():

	# collect arguments
	server_ip, server_port, username = util.client_util.fetch_args(sys.argv)
	
	# TODO: request login to server
	
	try:
		client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		client_socket.connect((server_ip, server_port))
	except socket.error as e:
		print(Error.no_server_error)
		client_socket.close()
		sys.exit()
	try:
		register = {}
		#client_socket.connect((server_ip, server_port))
		register['cmd'] = 'register'
		register['username'] = username
		client_socket.send(json.dumps(register).encode())
		response = client_socket.recv(2048)
		response = response.decode()
		if not response == 'Success':
			print(Error.user_already_logged_in)
			client_socket.close()
			sys.exit()
		print(Success.successful_login)
		receive_thread = threading.Thread(target=receive_from_server, args=(client_socket,), name='Thread-receive', daemon=True)
		receive_thread.start()
		obj={}
		while True:
			cmd = input('')
			cmd = re.findall(r'[^"\s]\S*|".+?"', cmd)
			if cmd[0] == 'tweet':
				postTwitter(cmd, client_socket)
			elif cmd[0] == 'subscribe':
				obj['cmd'] = 'subscribe'
				obj['hashtag'] = cmd[1][1:]
				client_socket.send(json.dumps(obj).encode())
			elif cmd[0] == 'unsubscribe':
				obj['cmd'] = 'unsubscribe'
				obj['hashtag'] = cmd[1][1:]
				client_socket.send(json.dumps(obj).encode())
			elif cmd[0] == 'timeline':
				obj['cmd'] = 'timeline'
				client_socket.send(json.dumps(obj).encode())
			elif cmd[0] == 'getusers':
				obj['cmd'] = 'getusers'
				client_socket.send(json.dumps(obj).encode())
			elif cmd[0] == 'gettweets':
				obj['cmd'] = 'gettweets'
				obj['username'] = cmd[1]
				client_socket.send(json.dumps(obj).encode())
			elif cmd[0] == 'exit':
				obj = {}
				obj['cmd'] = 'exit'
				client_socket.send(json.dumps(obj).encode())
				print('bye bye')
				break
		client_socket.close()
	except socket.error as e:
		# shouldn't happend
		sys.exit()


	# TODO: listen to command: tweet, subscribe, unsubscribe, timeline, getusers, gettweets, exit

def receive_from_server(socket):
	while True:
		response = socket.recv(50000)
		response = response.decode()
		print(response)


def postTwitter(cmd, client_socket):
	obj={}
	cmd[1] = cmd[1][1:-1]
	# tweet​ “<150 char max tweet>” <Hashtag>
	# check no message or message len = 0
	if len(cmd) < 3 or len(cmd[1]) == 0:
		print(Error.illegal_msg_len_none)
	# check messag length
	elif len(cmd[1]) > 150:
		print(Error.illegal_msg_len)
	else:
		if not cmd[2].startswith('#'):
			print(Error.illegal_hashtag)
			return
		hashtags = cmd[2].split('#')
		for hashtag in hashtags[1:]:
			if not hashtag or not hashtag.isalnum():
				print(Error.illegal_hashtag)
				return
		obj['cmd'] = 'tweet'
		obj['message'] = cmd[1]
		obj['hashtags'] = cmd[2]
		client_socket.send(json.dumps(obj).encode())


if __name__ == '__main__':
	main()
