class User:
    def __init__(self, username, socket):
        self.username = username
        self.tags_subscribed = []
        self.tweets_posted = []
        self.socket = socket
    
    def add_tweet_posted(self, tweet):
        """Adds a tweet to the user pbject

        Args:
            tweet: the tweet posted by the user, a Tweet object
        """
        self.tweets_posted.append(tweet)
    
    def add_tag_subscribed(self, tag):
        """Adds a hashtag subscription to the user pbject

        Args:
            tag: the hashtag the user requested to subscribe to, a string, e.g. 'hello'
        """
        self.tags_subscribed.append(tag)


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
    
    def push_format(self):
        """Formats the tweet for push

        Format the tweet in the following format
        <sender_username>: "<tweet_message>" <origin_hashtag>

        Return:
            formatted_tweet: the formatted tweet, a string
        """
        original_tag = ''.join(self.tags_attached)
        formatted_tweet = '{}: "{}" {}'.format(self.from_user, self.message, original_tag)
        return formatted_tweet

