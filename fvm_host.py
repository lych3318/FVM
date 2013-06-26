from pylvm2.lvm_ctrl import *
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
		self.lvm = LVM2()
		self.lvm.load()
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
					nodelist[0].login()
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
		dirpath = cfg['root']+'/'+name
		command = 'rm -r '+dirpath
		os.system(command)
		
	def CreateVolume(self, lv_name, size, volgroup):
		self.lvm.lv_create(volgroup, lv_name, size)
		return '/dev/mapper/'+volgroup+'-'+lv_name

	def RemoveVolume(self, dev):
		self.lvm.lv_remove(dev)

	def CreateCacheDev(self, devname, ssd_dev, disk_dev, size):
		command = 'flashcache_create -p back -s %sM %s %s %s' % (size, devname, ssd_dev, disk_dev)
		os.system(command)
		return '/dev/mapper/'+devname

	def DestroyCacheDev(self, ssd_dev):
		command = 'flashcache_destroy %s' % (ssd_dev)
		os.system(command)

	def LoadCacheDev(self, ssd_dev):
		command = 'flashcache_load '+ssd_dev
		os.system(command)

	def IsDevExists(self, dev):
		return os.path.exists(dev)

	#def MountVolume(self, name, size, volgroup):
	def MountVolume(self, name, **kwargs):
		disk_name = name+'_disk'
		ssd_name = name+'_ssd'
		cachedev_name = name+'_cachedev'
		if volume_dev.has_key(disk_name):#this volume has been connected before
			disk_dev = volume_dev[disk_name]
			if not self.IsDevExists(disk_dev):#check if the volume is being connected
				path = '/root/workspace/FVM/data/remote_volume'
				ReadFile(path, remote_volume)
				addr = remote_volume[name]
				print name, addr
				disk_dev = self.TargetLogin(addr, 'fvm_'+name)
				volume_dev[disk_name] = disk_dev
				print disk_dev
		else:
			path = '/root/workspace/FVM/data/remote_volume'
			ReadFile(path, remote_volume)
			addr = remote_volume[name]
			print name, addr
			disk_dev = self.TargetLogin(addr, 'fvm_'+name)
			volume_dev[disk_name] = disk_dev
			print disk_dev

		if volume_dev.has_key(ssd_name):# check if the ssd cache has been created
			ssd_dev = volume_dev[ssd_name]
			#flashcache_load
			self.LoadCacheDev(ssd_dev)
			#flashcache_load
		else:
			size = kwargs['size']
			volgroup = kwargs['volgroup']
			# flashcache_create
			ssd_dev = self.CreateVolume('fvm_cache_'+name, size, volgroup)
			cachedev = self.CreateCacheDev('fvm_cachedev_'+name, ssd_dev, disk_dev, size)
			# flashcache_create
			volume_dev[ssd_name] = ssd_dev
			volume_dev[cachedev_name] = cachedev

		cachedev = volume_dev[cachedev_name]
		dirpath = self.MkDir(name)
		command = 'mount '+cachedev+' '+dirpath
		os.system(command)

		path = '/root/workspace/FVM/data/volume_dev'
		WriteFile(path, volume_dev)

	def UmountVolume(self, name):
		cachedev_name=name+'_cachedev'
		addr = remote_volume[name]
		cachedev = volume_dev[cachedev_name]
		command = 'umount '+cachedev
		os.system(command)
		self.RmDir(name)		
		self.TargetLogout(addr, 'fvm_'+name)

	def CleanCache(self, dev):
		command = 'flashcache_invalidate '+dev
		os.system(command)
