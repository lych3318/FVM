from fvm_client import *

# fvmclient = FVMClient()
# def DoAction(action, args):
# 	if action=='register':
# 		fvmhost.MountVolume(args[0], args[1])

# def ProcessMSG(msg):
# 	pass

if __name__=='__main__':
	msgservice = MsgService()
	def serve(sock, addr):
		msgservice.recvmsg(sock)

	host = '192.168.0.155'
	port = 5921
	print 'starting message service on %s:%s\n' % (host, port)
	msgserver = StreamServer((host,port), serve)
	msgserver.serve_forever()