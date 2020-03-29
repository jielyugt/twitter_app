import sys
import socket
from objects import User, Tweet

# collect login arguments
def fetch_args(argv):
	if len(argv) != 2:
		sys.exit()
    port = argv[2]
	try:
		port = int(port)
		if port < 1024 or port > 65535:
			raise Exception('invalid range')
	except:
		sys.exit()
	return port

def tag_to_user(tags, users):
    """find subscribers

    Given a list of hashtags, return the users who subscribe to them
    
    Args:
        tags: a list of string, e.g. ['#hello','#world']
        users: current users on the server, a list of User objects

    Returns:
        subscribers: a list of User objects
    """
    subscribers = set()
    for tag in tags:
        for user in users:
            if tag in user.tags_subscribed:
                subscribers.add(user)
    return list(subscribers)

def register_user(username, socket, socket_user):
    """register a new user

    Add user info to socket_user dictionay
    
    Args:
        username: a string
        socket: a Socket object
        socket_user: a dict of socket connection -> user object

    Returns:
        False if user already exists, True if successful
    """
    if username in socket_user.values:
        return False
    socket_user[socket] = User(username, socket)
    return True

def push_tweet(users, tweet, waitlist, message_queues):
    """push a tweet to a list of users
    
    Args:
        users: a list of User objects
        tweet: a Tweet object
        waitlist: queue for select() method, a list
        message_queues: dictionary of queues for messages, a dict of socket -> queue of Tweet object
    """
    for user in users:
        waitlist.append(user.socket)
        if user.socket not in message_queues:
            message_queues[socket] = [tweet]
        else:
            message_queues[socket].append(tweet)

