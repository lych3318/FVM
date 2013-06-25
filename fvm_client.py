from pylvm2.lvm_ctrl import *
from pytgt.tgt_ctrl import *
import iscsi.scandev
from msgservice import *
import os, random

cfg = {}
target = {}

def WriteFile(path, cfg):
	fp = open(path, 'w')
	for key in cfg.keys():
		line = key+' '+cfg[key]+'\n'
		fp.write(line)

class FVMClient():
	def __init__(self):
		self.lvm = LVM2()
		self.lvm.load()
		self.tgt = Tgt()
		self.load('/root/workspace/FVM/data/cfg_client')

	def load(self, config_file):
		fp = open(config_file)
		while True:
			line = fp.readline()
			if len(line) == 0:
				break;
			key, value = line.split()
			cfg[key] = value
		print cfg

	def config(self, addr, port, name, hostaddr, hostport):
		cfg['addr']=addr
		cfg['port']=port
		cfg['name']=name
		cfg['hostaddr']=hostaddr
		cfg['hostport']=hostport
		path='/root/workspace/FVM/data/cfg_client'
		WriteFile(path, cfg)

	def register(self):
		msg = 'register '+cfg['name']+' '+cfg['addr']+' '+cfg['port']
		self.SendMessage(cfg['hostaddr'], int(cfg['hostport']), msg)

	def create_snapshot(self, original_dev, snap_name, size):
		self.lvm.lv_create_snapshot(original_dev, snap_name, size)
		self.snap_name = snap_name

	def remove_snapshot(self, dev):
		self.lvm.lv_remove(dev)

	def create_target(self, lun_path, target_name):
		acl = 'all'
		lun_index = '1'
		while True:
			target_id = str(random.randint(0,1024))
			if not self.tgt.is_in_targetlist(target_id):
				break 
		self.tgt.new_target(target_id, target_name)
		self.tgt.bind_target(target_id, acl)
		self.tgt.new_lun(target_id, lun_path, lun_index)
		self.target_id = target_id
		self.target_name = target_name

	def remove_target(self, target_name):
		target_id = self.tgt.target_name2target_id(target_name)
		if target_id == None:
			print 'No such target'
			return
		if self.tgt.delete_target(target_id) != None:
			print 'failed to Disassemble Volume' + target_name

	def AssembleVolume(self, dev, name, size):
		self.create_snapshot(dev, 'snap_'+name, size)
		self.create_target(dev, 'fvm_'+name)
		self.original_volume = dev
		self.volgroup = (os.path.basename(dev).split('-'))[0]
		self.prefix = os.path.dirname(dev)+'/'+self.volgroup
		self.PrintStatus()

	def DisassembleVolume(self, name):
		target_name = 'fvm_'+name
		snap_name = self.prefix+'-snap_'+name
		self.remove_target(target_name)
		self.remove_snapshot(snap_name)

	def SendMessage(self, addr, port, msg):
		sock = socket.socket()
		sock.connect((addr,port))
		msgservice = MsgService()
		msgservice.sendmsg(sock, msg)

	# def VolumeUpdata(self):
	# 	msg = 'volume updata start'
	# 	self.message(host_addr, host_port, msg)
	# 	# ret = self.message()
	# 	# if ret = -1:
	# 	# 	print 'Updata failed\n'
	# 	self.remove_target()
	# 	self.remove_snapshot()
	# 	self.create_snapshot()
	# 	self.create_target()
	# 	msg = 'volume updata finished'
	# 	self.message(host_addr, host_port, msg)

	def PrintStatus(self):
		print 'original volume: '+self.original_volume
		print 'snapshot volume: '+self.snap_name
		print 'target id:       '+self.target_id
		print 'target name:     '+self.target_name
