import sys
import socket
import select
from util.messages import Error, Success
import util.server_util
from util.objects import User, Tweet
import json


### Main Function

def main():
	
	# collect arguments
	server_port = util.server_util.fetch_args(sys.argv)

	# bind socket to port
	server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
		server_socket.bind(('localhost', server_port))
	except:
		sys.exit()
	server_socket.listen(5)

	# prepare data structures
	socket_users = {}               # dict of socket connection -> user object

	# select
	potential_readers = [server_socket]
	potential_writers = []
	potential_errors = []
	message_queues = {}             # dict of socket -> queue of Tweet object

	while True:
		ready_to_read, ready_to_write, in_error = \
				select.select(
					potential_readers,
					potential_writers,
					potential_errors)
		
		for s in ready_to_read:

			# if a connection from a new client is requested
			if s is server_socket:
				print('got connection')
				client_connection, client_address = s.accept()
				potential_readers.append(client_connection)

			# if a already connected client sends a request
			else:
				raw_data = s.recv(2048)
				dic_data = json.loads(raw_data.decode())
				cmd = dic_data['cmd']

				if cmd == 'register':
					username = dic_data['username']

					# register user if no duplicate username
					status = 'Success'
					if not util.server_util.register_user(username, s, socket_users):
						status = 'Error'
					print(username, status)
					# send status code
					util.server_util.send_msg_socket([s],
													status,
													potential_writers,
													message_queues)

				if cmd == 'tweet': 
					message = dic_data['message']
					hashtags = dic_data['hashtags']

					# add tweet to user history
					tag_list = hashtags.strip('#').split('#')
					tweet = Tweet(socket_users[s], message, tag_list)
					socket_users[s].tweets_posted.append(tweet)

					# find out subscribers to the hashtags
					subscribers = util.server_util.tag_to_user(tag_list, list(socket_users.values()))
					subscribers_sockets = [user.socket for user in subscribers]

					# push tweets
					util.server_util.send_msg_socket(subscribers_sockets, 
													tweet.push_format(), 
													potential_writers, 
													message_queues)

				elif cmd == 'subscribe':
					# TODO
					pass
				#TODO
		
		for s in ready_to_write:
			message_queue = message_queues[s]
			try:
				message_to_send = message_queue.pop(0)
			except:
				print('Debug: poping from empty list. should not ever trigger this error. if triggered, check logics.')
			else:
				s.send(message_to_send.encode())
			
			if len(message_queue) == 0:
				potential_writers.remove(s)
				

if __name__ == '__main__':
	main()

# Below are related and useful links
# Python Select: https://docs.python.org/3/library/select.html
# Handle multiple clients with select: https://steelkiwi.com/blog/working-tcp-sockets/