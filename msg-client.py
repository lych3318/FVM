import gevent.socket as socket
from msgservice import MsgService
from gevent.pool import Pool
import gevent

def test():
	addr = '192.168.0.155'
	port = 5921
	def robot(index, addr, port):
		sock = socket.socket()
		sock.connect((addr,port))
		print 'connection %s' % (index)
		while True:
			msgservice = MsgService()
			msg = 'hello, this msg coming from clent %s\n' % (index)
			msgservice.sendmsg(sock, msg)
			gevent.sleep(3)

	print 'creating connections\n'
	count = 10
	pool = Pool(10)
	for i in range(count):
		pool.spawn(robot, i, addr, port)
	pool.join()

if __name__ == '__main__':
	test()