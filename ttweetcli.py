import sys
import socket
from util.messages import Error, Success
import util.client_util


def main():

	# collect arguments
	server_ip, server_port, username = util.client_util.fetch_args(sys.argv)
	
	# TODO: request login to server
	client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	# TODO: listen to command: tweet, subscribe, unsubscribe, timeline, getusers, gettweets, exit


if __name__ == '__main__':
	main()
