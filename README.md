# twitter_app

Spring 2020 CS3251 Computer Networks I Programming  Assignment 2

## File Description

* util
  * client_util.py: helper functions for ttweetcli.py
  * messages.py: output messages
* README.md
* project_description.pdf
* ttweetcli.py: client application
* ttweetser.py: server application

## How to Run

### Start the server application:
python3 ttweetser.py <port_number>

### Start the client application
python3 ttweetcli.py <ServerIP> <ServerPort> <Username>
  
### Use the client applciation
Available commands for client: tweet, subscribe, unsubscribe, timeline, getusers, gettweets, exit

## Team Members

* Haoran Xin: I did blablabla
* Jie Lyu: I did blablabla
* Junyan Mao: I did blablabla

## issue

* client: handle escape char
* server
  * gettweets: give "no user Username in the system" back to client
  * all tweets should have # 
  * follow the server side ouput format in txt
