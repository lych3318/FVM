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
volume_dev = {}

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
		path='/root/workspace/FVM/data/remote_volume'
		ReadFile(path, remote_volume)
		#This is valid when is the program restart, not system reboot
		path='/root/workspace/FVM/data/volume_dev'
		ReadFile(path, volume_dev)

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
					return '/dev/'+scandev.get_blockdev_by_targetname(nodelist[0].name)
			print 'Target %s not found!' % (target_name)
		else:
			print 'no node found!'

	def TargetLogout(self, addr, target_name):
		nodelist = libiscsi.discover_sendtargets(addr)
		if nodelist is not None :
			for node in nodelist:
				if node.name == target_name:
					nodelist[0].logout()		

	def MkDir(self, dirname):
		#command = 'mkdir '+cfg['root']+'/'+dirname
		#subprocess(command)
		#return cfg['root']+'/'+dirname
		dirpath = cfg['root']+'/'+dirname
		os.mkdir(dirpath)
		return dirpath

	def RmDir(self, name):
		devpath = volume_dev[name]
		dirpath = volume_dev[devpath]
		command = 'rm -r '+dirpath
		os.system(command)

	def MountVolume(self, name):
		path = '/root/workspace/FVM/data/remote_volume'
		ReadFile(path, remote_volume)
		addr = remote_volume[name]
		print name, addr
		devpath = self.TargetLogin(addr, 'fvm_'+name)
		volume_dev[name] = devpath
		print devpath

		dirpath = self.MkDir(name)
		command = 'mount '+devpath+' '+dirpath
		os.system(command)
		volume_dev[devpath] = dirpath

		path = '/root/workspace/FVM/data/volume_dev'
		WriteFile(path, volume_dev)

	def UmountVolume(self, name):
		addr = remote_volume[name]
		devpath = volume_dev[name]
		command = 'umount '+devpath
		os.system(command)
		self.RmDir(name)		
		self.TargetLogout(addr, 'fvm_'+name)

	def CleanCache(self, dev):
		command = 'flashcache_invalidate '+dev
		os.system(command)
