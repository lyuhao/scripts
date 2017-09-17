#!/usr/bin/env python
import socket
import sys
from threading import Thread
from SocketServer import ThreadingMixIn

class ClientThread(Thread):
	def __init__(self,ip,port,line):
		Thread.__init__(self)
		self.ip = ip
		self.port = port 
		print "[+] New thread started for"+ip+":"+str(port)
	def run(self):
		sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		server_address = (self.ip,self.port)
		sock.connect(server_address)
		##message = 'This is the message. It will be repeated\n'
		message = line
		print >>sys.stderr, 'sending "%s" ' % message
		sock.sendall(message)

		amount_received = 0 
		amount_expected = len(message)
		data = sock.recv(len(message))
		print >>sys.stderr, 'received "%s"' %data
		sock.close

port = int(sys.argv[1])



for i in range(0,10000):
	line = str(i)+' '+str(i)+' '+str(i)+'\n'
	newthread = ClientThread('localhost',port,line)
	newthread.start()
	newthread.join()