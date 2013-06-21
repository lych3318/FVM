from gevent.server import StreamServer
import gevent.socket as socket
from msgservice import MsgService

msgservice = MsgService()

def serve(sock, addr):
	msgservice.recvmsg(sock)

host = '0.0.0.0'
port = 5921
print 'starting message service on %s:%s\n' % (host, port)
msgserver = StreamServer((host,port), serve)
msgserver.serve_forever()
