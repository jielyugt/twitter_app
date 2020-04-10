import enum 
  
class Error(enum.Enum): 
	# 1. Server IP invalid: “error: server ip invalid, connection refused.”
    invalid_ip = 'error: server ip invalid, connection refused.'
    # 2. Server Port invalid: “error: server port invalid, connection refused.”
    invalid_port = 'error: server port invalid, connection refused.'
    # 3. Username is invalid: “error: username has wrong format, connection refused.”
    invalid_username = 'error: username has wrong format, connection refused.'
    # 4. User is already logged in: “username illegal, connection refused.”
    user_already_logged_in = 'username illegal, connection refused.'
    # 5. Wrong number of parameters: “error: args should contain <ServerIP> <ServerPort> <Username>”
    wrong_param = 'error: args should contain <ServerIP> <ServerPort> <Username>'
    # 6. Illegal message length(>150): “message length illegal, connection refused.”
    illegal_msg_len = 'message length illegal, connection refused.'
    # 7. Illegal message length(=0 or None): “message format illegal.”
    illegal_msg_len_none = 'message format illegal.'
    # 8. Illegal hashtag: “hashtag illegal format, connection refused.”
    illegal_hashtag = 'hashtag illegal format, connection refused.'
    # 9. Maximum hashtags reached: “operation failed: sub <hashtag> failed, already exists or exceeds 3 limitation”
    max_hashtag_reached = 'operation failed: sub <hashtag> failed, already exists or exceeds 3 limitation'
    # 10. try to connect but no server is running
    no_server_error = 'connection error, please check your server: Connection refuseds'

    def __str__(self):
        return str(self.value)

class Success(enum.Enum):
    # 1. If the user manages to log in: “username legal, connection established.”
    successful_login = 'username legal, connection established.'
    # 2. User exits successfully (no full stop): “bye bye”
    successful_exit = 'bye bye'
    # 3. For any subscribe/unsubscribe operations that succeeds (no full stop): “operation success”
    successful_operation = 'operation success'
    # 4. For tweet operation, no feedback needed
    pass
    
    def __str__(self):
        return str(self.value)



