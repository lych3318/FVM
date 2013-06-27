from fvm_host import *
from gevent.server import StreamServer
import gevent.socket as socket
from msgservice import MsgService

remote_volume={}

# fvmhost = FVMHost()
# def DoAction(action, args):
# 	if action=='mount':
# 		fvmhost.MountVolume(args[0], args[1])
# 	elif action=='register':
# def WriteFile(path, key, value):
# 	fp = open(path, 'a')
# 	line = key+' '+value+'\n'
# 	fp.write(line)
def ReadFile(path, dic):
	fp = open(path)
	while True:
		line = fp.readline()
		if len(line) == 0:
			break;
		key, value = line.split()
		dic[key] = value

def WriteFile(path, dic):
	fp = open(path, 'w')
	for key in dic.keys():
		line = key+' '+dic[key]+'\n'
		fp.write(line)

msgservice = MsgService()
def ProcessMSG(msg):
	args = msg.split()
	if args[0] == 'register':
		path = '/root/workspace/FVM/data/remote_volume'
		remote_volume[args[1]+'_addr'] = args[2]
		remote_volume[args[1]+'_port'] = args[3]
		remote_volume[args[1]+'_uuid'] = args[4]
		WriteFile(path, remote_volume)
	elif args[0] == 'updata':
		fvmhost = FVMHost()
		fvmhost.UmountVolume(args[1])
		del fvmhost

		msg_back = 'finished'	
		addr = remote_volume[args[1]+'_addr']
		port = int(remote_volume[args[1]+'_port'])
		sock = socket.socket()
		print addr, port
		sock.connect((addr, port))
		#sock.connect(('localhost', 5922))
		#sock.connect(('192.168.0.155', 5922))
		msgservice = MsgService()
		print 'sending message----------------------------------------'
		msgservice.sendmsg(sock, msg_back)
		sock.close()
	elif args[0] == 'updata_finished'
		fvmhost = FVMHost()
		fvmhost.MountVolume(args[1])
		del fvmhost

def load():
	path = '/root/workspace/FVM/data/remote_volume'
	ReadFile(path, remote_volume)
	print remote_volume

if __name__=='__main__':
	load()
	def serve(sock, addr):
		msg = msgservice.recvmsg(sock)
		ProcessMSG(msg)

	host = '0.0.0.0'
	port = 5921
	msgserver = StreamServer((host,port), serve)
	msgserver.serve_forever()