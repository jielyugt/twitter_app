import sys
import socket
from util.messages import Error, Success
import util.client_util
import shlex
import json



def main():

	# collect arguments
	server_ip, server_port, username = util.client_util.fetch_args(sys.argv)
	
	# TODO: request login to server
	client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
		register = {}
		client_socket.connect((server_ip, server_port))
		register['cmd'] = 'register'
		register['username'] = username
		client_socket.send(json.dumps(register).encode())
		response = client_socket.recv(2048)
		response = response.decode()
		if not response == 'Success':
			print(Error.invalid_username)
			sys.exit()
		# after validate username:
		print(Success.successful_login)
		while True:
			cmd = input('user ' + username +' stdin command: ')
			cmd = shlex.split(cmd)
			if cmd[0] == 'tweet':
				# tweet​ “<150 char max tweet>” <Hashtag>
				# check no message or message len = 0
				# '""'
				if len(cmd) < 3 or len(cmd[1]) == 0:
					print(Error.illegal_msg_len_none)
					continue
				# check messag length
				elif len(cmd[1]) > 150:
					print(Error.illegal_msg_len)
					continue
				else:
					if not cmd[2].startswith('#'):
						print(cmd[2])
						print(Error.illegal_hashtag)
						continue
					hashtags = cmd[2].split('#')
					for hashtag in hashtags[1:]:
						if not hashtag or not hashtag.isalnum():
							print(Error.illegal_hashtag)
							continue;
					postTwitter()
			elif cmd[0] == 'subscribe':
				subscribe()
			elif cmd[0] == 'unsubscribe':
				unsubscribe()
			elif cmd[0] == 'timeline':
				timeline()
			elif cmd[0] == 'getusers':
				getusers()
			elif cmd[0] == 'gettweets':
				get_tweet()
			elif cmd[0] == 'exit':
				print('bye bye')
				break
		client_socket.close()

					



	except socket.error as e:
		# shouldn't happend
		print(str(e))


	# TODO: listen to command: tweet, subscribe, unsubscribe, timeline, getusers, gettweets, exit

def postTwitter():
	pass

def subscribe():
	pass

def unsubscribe():
	pass

def timeline():
	pass

def getusers():
	pass

def get_tweet():
	pass


if __name__ == '__main__':
	main()
