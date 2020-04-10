class User:
	def __init__(self, username, socket):
		"""
		Args:
			username: a string
			socket: a Socket object
		"""
		self.username = username
		self.tags_subscribed = []
		self.tweets_posted = []
		self.socket = socket
		self.timeline = ''              # tweets pushed to the user
	
	def add_tag_subscribed(self, tag):
		"""subscribe a user to a hashtag

		1. #ALL​ subscribes the client to all hashtags so it should receive all new tweets
		2. A client should be able to subscribe to up to 3 hashtags​
		3. subscribe to a hashtag that is already subscribed has no effects

		Args:
			tag: the hashtag the user requested to subscribe to, a string, e.g. 'hello'

		Returns:
			True if successful, False if failed
		"""
		if tag in self.tags_subscribed:
			return True

		if len(self.tags_subscribed) >= 3:
			return False
		self.tags_subscribed.append(tag)
		return True
	
	def add_to_timeline(self, tweet):
		self.timeline += tweet.timeline_format() + '\n'

	def remove_tag_subscribed(self, tag):
		"""unsubscribe a user from a hashtag

		1. #ALL ​will unsubscribe ​this client​ from all hashtags (including the other 2 hashtags that could be added on top of the #ALL)
		2. Unsubscribe command should have no effect if it refers to a # that has not been subscribed to previously.

		Args:
			tag: the hashtag the user requested to unsubscribe from, a string, e.g. 'hello'
		
		Returns:
			None, since it cannot fail
		"""
		if tag in self.tags_subscribed:
			if tag == 'ALL':
				self.tags_subscribed = []
			else:
				self.tags_subscribed.remove(tag)
	
	def get_tweets(self):
		"""get all the tweets posted from a user
		
		Returns:
			tweets: a string
		"""
		tweets = ''
		for each in self.tweets_posted:
			tweets += each.timeline_format() + '\n'
		tweets = tweets.strip('\n')
		return tweets


class Tweet:
	def __init__(self, user, message, tags):
		"""
		Args:
			user: the user how posted the tweet, a User object
			message: the message body, a string e.g. 'today is a good day'
			tags: the tags attached to the tweet, a list of string, e.g. ['hello','world']
		"""
		self.message = message
		self.tags_attached = tags
		self.from_user = user
	
	def timeline_format(self):
		"""Formats the tweet for timeline

		Format the tweet in the following format
		<sender_username>: "<tweet_message>" <origin_hashtag>

		Return:
			formatted_tweet: the formatted tweet, a string
		"""
		original_tag = ''.join(self.tags_attached)
		formatted_tweet = '{}: "{}" {}'.format(self.from_user.username, self.message, '#'+original_tag)
		return formatted_tweet
	
	def push_format(self):
		"""Formats the tweet for push

		Format the tweet in the following format
		<sender_username> "<tweet_message>" <origin_hashtag>

		Return:
			formatted_tweet: the formatted tweet, a string
		"""
		original_tag = ''.join(self.tags_attached)
		formatted_tweet = '{} "{}" {}'.format(self.from_user.username, self.message, '#'+original_tag)
		return formatted_tweet

