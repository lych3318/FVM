# from fvm_host import *
from gevent.server import StreamServer
import gevent.socket as socket
from msgservice import MsgService

remote_volume={}

# fvmhost = FVMHost()
# def DoAction(action, args):
# 	if action=='mount':
# 		fvmhost.MountVolume(args[0], args[1])
# 	elif action=='register':
def WriteFile(path, key, value):
	fp = open(path, 'a')
	line = key+' '+value+'\n'
	fp.write(line)

def ProcessMSG(msg):
	args = msg.split()
	if args[0] == 'register':
		path = '/root/workspace/FVM/data/remote_volume'
		remote_volume[args[1]] = args[2]
		WriteFile(path, args[1], args[2])

if __name__=='__main__':
	msgservice = MsgService()
	def serve(sock, addr):
		msg = msgservice.recvmsg(sock)
		ProcessMSG(msg)

	host = '0.0.0.0'
	port = 5921
	msgserver = StreamServer((host,port), serve)
	msgserver.serve_forever()