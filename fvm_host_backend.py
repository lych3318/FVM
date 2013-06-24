from fvm_host import *

remote_volume={}

fvmhost = FVMHost()
def DoAction(action, args):
	if action=='mount':
		fvmhost.MountVolume(args[0], args[1])
	elif action=='register':

def ProcessMSG(msg):
	pass

if __name__=='__main__':
	msgservice = MsgService()
	def serve(sock, addr):
		msgservice.recvmsg(sock)

	host = '0.0.0.0'
	port = 5921
	print 'starting message service on %s:%s\n' % (host, port)
	msgserver = StreamServer((host,port), serve)
	msgserver.serve_forever()