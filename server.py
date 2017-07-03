#!/usr/bin/env python

import socket
from threading import Thread
from threading import Lock
from SocketServer import ThreadingMixIn
from sets import Set
import time
from random import randint

globallock = Lock()


## id of the spark on this machine 
WorkerId = ""

Exit = False
## set of application on this machine 
AppSet = list()



class ClientThread(Thread):
	def __init__(self,ip,port,line):
		Thread.__init__(self)
		self.ip = ip
		self.port = port 
		self.line = line 

	def run(self):
		sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		server_address = (self.ip,self.port)
		sock.connect(server_address)
		message = self.line
		sock.sendall(message)


class Client(Thread):
	def __init__(self,period,ip,port):
		Thread.__init__(self)
		self.period = period
		self.ip = ip
		self.port = port 

	def run(self):
		number = 20
		for i in range(0,1000):
			if(Exit):
				return
			time.sleep(self.period)
			#print "here"
			#print "workerid is " + WorkerId
			if (WorkerId != ''):
				app_name = AppSet[0]
				diff = randint(0,2) - 1

				number = min(max(1,number+diff),20)
				line = WorkerId+' '+app_name+' '+str(number)+'\n'
				print line
				#newthread = ClientThread(self.ip,self.port,line)
				#newthread.start()
				#newthread.join()

class HandleThread(Thread):

	def __init__(self,ip,port):
		Thread.__init__(self)
		self.ip = ip
		self.port = port 
		print "[+] New thread started for"+ip+":"+str(port)

	def run(self):
		while not Exit:
			data = conn.recv(2048)
			if not data: break
			if data =="": break
			print "received data:", data
			#conn.send(data)
			dataarray = data.split(' ')
			globallock.acquire()
			name = dataarray[0]
			if (name == "app"):
				global AppSet
				Appname = dataarray[1]
				AppSet.append(Appname[:-1])
			else:
				global WorkerId
				WorkerId = dataarray[1]
				WorkerId = WorkerId[:-1]
			globallock.release()

TCP_IP = '0.0.0.0'
TCP_PORT = 9999
BUFFER_SIZE = 20 

tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcpsock.bind((TCP_IP, TCP_PORT))
threads = []

SERVER_PORT = 9990
SERVER_IP = "localhost"
client = Client(1,SERVER_IP,SERVER_PORT)
client.start()

try:
	while True:
		tcpsock.listen(4)
		(conn, (ip,port)) = tcpsock.accept()
		newthread = HandleThread(ip,port)
		newthread.start()
		threads.append(newthread)
except KeyboardInterrupt:
	print "Keyboard"
	Exit = True

for t in threads:
    t.join()

client.join()

