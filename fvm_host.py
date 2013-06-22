from gevent.server import StreamServer
import gevent.socket as socket
from msgservice import MsgService
import os
import libiscsi
import iscsi.scandev
import subprocess

def FVMHost():
	def __init__():
		pass

	def message():
		pass

	def TargetLogin(self, addr, target_name):
		nodelist = libiscsi.discover_sendtargets(addr)
		if nodelist is not None :
			for node in nodelist:
				if node.name == target_name:
					nodelist[0].login()
					return scandev.get_blockdev_by_targetname(nodelist[0].name)
			print 'Target %s not found!' % (target_name)
		else:
			print 'no node found!'

	def TargetLogout(self, addr, target_name):
		nodelist = libiscsi.discover_sendtargets(addr)
		if nodelist is not None :
			for node in nodelist:
				if node.name == target_name:
					nodelist[0].logout()		

	def MountVolume(self, dev, dir_root):
		command = 'mount '+dev+' '+dir_root
		subprocess(command)

	def UmountVolume(self, dev):
		command = 'Umount '+dev
		subprocess(command)

	def CleanCache(self, dev):
		command = 'flashcache_invalidate '+dev
		subprocess(command)

msgservice = MsgService()
def serve(sock, addr):
	msgservice.recvmsg(sock)

host = '0.0.0.0'
port = 5921
print 'starting message service on %s:%s\n' % (host, port)
msgserver = StreamServer((host,port), serve)
msgserver.serve_forever()