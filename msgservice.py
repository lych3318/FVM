from gevent.server import StreamServer
import gevent.socket as socket

class MsgService():
	def __init__(self):
		pass

	def sendmsg(self, sock, msg):
		sock.sendall(msg)

	def recvmsg(self, sock):
		fp = sock.makefile()
		while 1:
			line = fp.readline()
			print 'msg received is: ' + line
			if not line:
				break
			return line

	def quit(self, sock):
		sock.close()