from gevent.server import StreamServer
import gevent.socket as socket
from msgservice import MsgService
import iscsi.scandev as scandev
import os
import libiscsi
import iscsi.scandev
import subprocess

cfg = {}
remote_volume = {}

def WriteFile(path, dic):
	fp = open(path, 'w')
	for key in dic.keys():
		line = key+' '+dic[key]+'\n'
		fp.write(line)

def ReadFile(path, dic):
	fp = open(path)
	while True:
		line = fp.readline()
		if len(line) == 0:
			break;
		key, value = line.split()
		dic[key] = value

class FVMHost():
	def __init__(self):
		self.load()

	def load(self):
		path='/root/workspace/FVM/data/cfg_host'
		ReadFile(path, cfg)

	def config(self, addr, port, name, root):
		path='/root/workspace/FVM/data/cfg_host'
		cfg['addr']=addr
		cfg['port']=port
		cfg['name']=name
		cfg['root']=root
		WriteFile(path, cfg)

	def TargetLogin(self, addr, target_name):
		nodelist = libiscsi.discover_sendtargets(addr)
		if nodelist is not None :
			for node in nodelist:
				if node.name == target_name:
					#nodelist[0].login()
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

	def MountVolume(self, name):
		path = '/root/workspace/FVM/data/remote_volume'
		ReadFile(path, remote_volume)
		addr = remote_volume[name]
		print name, addr
		devname = self.TargetLogin(addr, 'fvm_'+name)
		print devname
		# command = 'mount '+dev+' '+
		# subprocess(command)

	def UmountVolume(self, dev):
		command = 'Umount '+dev
		subprocess(command)
		self.TargetLogout(addr, name)

	def CleanCache(self, dev):
		command = 'flashcache_invalidate '+dev
		subprocess(command)
