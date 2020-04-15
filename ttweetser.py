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
		server_socket.close()
		sys.exit()
	server_socket.listen(5)

	# prepare data structures
	socket_users = {}               # dict of socket connection -> user object
	message_queues = {}             # dict of socket -> queue of Tweet object

	# select
	potential_readers = [server_socket]
	potential_writers = []
	potential_errors = []

	print('ready for requests and commands')
	while True:
		ready_to_read, ready_to_write, in_error = \
				select.select(
					potential_readers,
					potential_writers,
					potential_errors)

		for s in ready_to_read:

			# if a connection from a new client is requested
			if s is server_socket:
				print('new connect request received')
				client_connection, client_address = s.accept()
				potential_readers.append(client_connection)

			# if a already connected client sends a request
			else:
				raw_data = s.recv(2048)

				# client exited through Conrol C or errored out becasue of duplicate username
				if not raw_data:
					print('someone already closed its socket')
					potential_readers.remove(s)
					if s in socket_users:
						del socket_users[s]
					if s in message_queues:
						del message_queues[s]
					if s in potential_writers:
						potential_writers.remove(s)
					continue

				dic_data = json.loads(raw_data.decode())
				print('new command received', dic_data)
				cmd = dic_data['cmd']

				if cmd == 'register':
					# NOTE input: {'cmd':'register','username':'Tom'}
					# NOTE return: 'Success' if operation successful, 'Error' if username already exists
					username = dic_data['username']

					# register user if no duplicate username
					status = 'Success'
					if not util.server_util.register_user(username, s, socket_users):
						status = 'Error'

					# send status code
					util.server_util.send_msg_socket([s],
													status,
													potential_writers,
													message_queues)
					print(username, 'login command' ,status)

				elif cmd == 'tweet':
					# NOTE input: {'cmd':'tweet','message':'Hello World','hashtags':'#hello#world'}
					# NOTE return: None
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
					# add tweets to timeline
					for each in subscribers:
						each.add_to_timeline(tweet)

					print(socket_users[s].username + ' tweet pushed to' , [each.username for each in subscribers])

				elif cmd == 'subscribe':
					# NOTE input: {'cmd':'subscribe','hashtag':'hello'}
					# NOTE return: 'Success' if operation successful, 'Error' if not
					hashtag = dic_data['hashtag']

					# try to subscribe the user to hashtag
					status = 'operation success'
					if not socket_users[s].add_tag_subscribed(hashtag):
						status = 'operation failed: sub ' +  '#' + hashtag  + ' failed, already exists or exceeds 3 limitation'
					# send status code
					util.server_util.send_msg_socket([s],
													status,
													potential_writers,
													message_queues)
					print(socket_users[s].username, 'subscribe request' ,status)

				elif cmd == 'unsubscribe':
					# NOTE input: {'cmd':'unsubscribe','hashtag':'hello'}
					# NOTE return: 'Success' if operation successful, 'Error' if not
					hashtag = dic_data['hashtag']

					# try to subscribe the user to hashtag
					status = 'operation success'
					socket_users[s].remove_tag_subscribed(hashtag)

					# send status code
					util.server_util.send_msg_socket([s],
													status,
													potential_writers,
													message_queues)
					print(socket_users[s].username, 'unsubscribe request' ,status)

				elif cmd == 'timeline':
					# NOTE input: {'cmd':'timeline'}
					# NOTE return: formatted timeline, a string

					util.server_util.send_msg_socket([s],
													socket_users[s].timeline.strip('\n'),
													potential_writers,
													message_queues)
					print(socket_users[s].username, 'timeline sent')

				elif cmd == 'getusers':
					# NOTE input: {'cmd':'getusers'}
					# NOTE return: formatted user list, a string

					user_list = util.server_util.get_users(socket_users)
					print(user_list)
					util.server_util.send_msg_socket([s],
													user_list,
													potential_writers,
													message_queues)
					print(socket_users[s].username, 'user list request sent')

				elif cmd == 'gettweets':
					# NOTE input: {'cmd':'gettweets','username':'Tom'}
					# NOTE return: if username exists, formatted user tweet histoty, else, 'Error'
					username = dic_data['username']

					# check if username exists
					target_user = None
					for user in socket_users.values():
						if user.username == username:
							target_user = user

					if target_user is None:
						util.server_util.send_msg_socket([s],
														'Error',
														potential_writers,
														message_queues)
						print(socket_users[s].username, 'requested tweet history from user', username, 'and user cannot be found')
					else:
						util.server_util.send_msg_socket([s],
														target_user.get_tweets(),
														potential_writers,
														message_queues)
						print(socket_users[s].username, 'requested tweet history from user', username, 'and user found')

				elif cmd == 'exit':
					print(socket_users[s].username, 'exited')
					potential_readers.remove(s)
					del socket_users[s]
					if s in message_queues:
						del message_queues[s]
					if s in potential_writers:
						potential_writers.remove(s)

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
				del message_queues[s]


if __name__ == '__main__':
	main()

# Below are related and useful links
# Python Select: https://docs.python.org/3/library/select.html
# Handle multiple clients with select: https://steelkiwi.com/blog/working-tcp-sockets/
# getusers output order: https://piazza.com/class/k530q3x9ywp55n?cid=373