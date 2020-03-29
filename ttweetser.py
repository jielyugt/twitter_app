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
		server_socket.bind((socket.gethostname(), server_port))
	except:
		sys.exit()
    
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
                client_connection, client_address = s.accept()
                potential_readers.append(client_connection)

            # if a already connected client sends a request
            else:
                # TODO: read the request, do action and respond
                str_data = s.recv(2048).decode()
                dic_data = json.loads(str_data)
                cmd = dic_data['cmd']

                if cmd = 'register':
                    username = dic_data['username']
                    # there is no way to pass in username when client calls connect(), so it's a seperate process
                    util.server_util.register_user(username, s, socket_users)

                if cmd = 'tweet': 
                    # TODO
                    message = dic_data['message']
                    hashtags = dic_data['hashtags']
                    tag_list = hashtags.strip('#').split('#')
                    tweet = Tweet(socket_users[s], message, tag_list)
                    subscribers = util.server_util.tag_to_user(tag_list, list(socket_users.values()))
                    util.server_util.push_tweet(subscribers, tweet, potential_writers, message_queues)

                elif cmd = 'subscribe':
                    # TODO
                #TODO
        
        for s in ready_to_write:
            tweet_queue = message_queues[s]
            try:
                tweet_to_send = tweet_queue.pop(0)
            except:
                print('Debug: poping from empty list. should not ever trigger this error. if triggered, check logics.')
            else:
                s.send(tweet_to_send.push_format())
            
            if len(tweet_queue) == 0:
                potential_writers.remove(s)
                

if __name__ == '__main__':
	main()

# Below are related and useful links
# Python Select: https://docs.python.org/3/library/select.html
# Handle multiple clients with select: https://steelkiwi.com/blog/working-tcp-sockets/