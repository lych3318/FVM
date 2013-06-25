from gevent.server import StreamServer
import gevent.socket as socket
from msgservice import MsgService
import os
import libiscsi
import iscsi.scandev
import subprocess

def readfile(path):
	fp = open(path)

class FVMHost():
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

	def MountVolume(self, dev, dir):
		self.TargetLogin(addr, name)
		command = 'mount '+dev+' '+
		subprocess(command)

	def UmountVolume(self, dev):
		command = 'Umount '+dev
		subprocess(command)
		self.TargetLogout(addr, name)

	def CleanCache(self, dev):
		command = 'flashcache_invalidate '+dev
		subprocess(command)
