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

## Implementation Ideas

### Server
* utilized select() function to handle multiple clients
* receive and send information to clients through TCP

### Client
* main program listens to user command
* send commands and details packed in json dictionaries through TCP
* daemon threads listens to server and print outputs

## Requirement
python >= 3.6.9

## How to Run

### Start the server application:
python3 ttweetser.py <port_number>

### Start the client application
python3 ttweetcli.py <ServerIP> <ServerPort> <Username>
  
### Use the client applciation
Available commands for client: tweet, subscribe, unsubscribe, timeline, getusers, gettweets, exit

## Team Members

* Haoran Xin: implemented ttweetcli.py
* Jie Lyu: implemented ttweetser.py
* Junyan Mao: I did blablabla
