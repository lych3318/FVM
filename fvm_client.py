from pylvm2.lvm_ctrl import *
from pytgt.tgt_ctrl import *
import iscsi.scandev
from msgservice import *
import os, random, subprocess

cfg = {}
target = {}

def WriteFile(path, dic):
	fp = open(path, 'w')
	for key in dic.keys():
		line = key+' '+dic[key]+'\n'
		fp.write(line)
	fp.close()

def ReadFile(path, dic):
	fp = open(path)
	while True:
		line = fp.readline()
		if len(line) == 0:
			break;
		key, value = line.split()
		dic[key] = value
	fp.close()
	print dic

def GetVolumeUUID(volume_path):
	argv = ['blkid', '-o', 'value', volume_path]
	process = subprocess.Popen(argv, stdout=subprocess.PIPE, shell=False)
	output = process.stdout.readline().split()[0]
	print output
	return output

class FVMClient():
	def __init__(self):
		self.lvm = LVM2()
		self.lvm.load()
		self.tgt = Tgt()
		self.load('/root/workspace/FVM/data/cfg_client', cfg)
		self.load('/root/workspace/FVM/data/target', target)

	def load(self, path, dic):
		ReadFile(path, dic)

	def config(self, addr, port, name, hostaddr, hostport):
		cfg['addr']=addr
		cfg['port']=port
		cfg['name']=name
		cfg['hostaddr']=hostaddr
		cfg['hostport']=hostport
		path='/root/workspace/FVM/data/cfg_client'
		WriteFile(path, cfg)

	def register(self):
		msg = 'register '+cfg['name']+' '+cfg['addr']+' '+cfg['port']+' '+target['UUID']
		self.SendMessage(cfg['hostaddr'], int(cfg['hostport']), msg)

	def create_snapshot(self, original_dev, snap_name, size):
		self.lvm.lv_create_snapshot(original_dev, snap_name, size)
		target['snap_dev'] = target['prefix']+'-'+snap_name

	def remove_snapshot(self, dev):
		return self.lvm.lv_remove(dev)

	# def create_target(self, lun_path, target_name):
	# 	self.tgt.tgt_setup_lun(target_name, lun_path)
	# 	target['target_name'] = target_name

	def create_target(self, lun_path, target_name):
		acl = 'ALL'
		lun_index = '1'
		while True:
			target_id = str(random.randint(0,10))
			if not self.tgt.is_in_targetlist(target_id):
				break 
		self.tgt.new_target(target_id, target_name)
		self.tgt.bind_target(target_id, acl)
		self.tgt.new_lun(target_id, lun_path, lun_index)
		target['target_id'] = target_id
		target['target_name'] = target_name

	#def remove_target(self, target_name):
		# target_id = self.tgt.target_name2target_id(target_name)
		# if target_id == None:
		# 	print 'No such target'
		# 	return
	def remove_target(self):
		target_id = target['target_id']
		if self.tgt.delete_target(target_id) != None:
			print 'failed to Disassemble target ' + target_id
			return False
		return True

	def AssembleVolume(self, dev, size):
		name = cfg['name']
		target['original_volume'] = dev
		target['UUID'] = GetVolumeUUID(dev)
		target['volgroup'] = (os.path.basename(dev).split('-'))[0]
		target['prefix'] = os.path.dirname(dev)+'/'+target['volgroup']
		target['size'] = size
		self.create_snapshot(dev, 'snap_'+name, size)
		self.create_target(target['prefix']+'-snap_'+name, 'fvm_'+name)
		path='/root/workspace/FVM/data/target'
		WriteFile(path, target)

	def DisassembleVolume(self):
		snap_dev = target['snap_dev']
		if not self.remove_target():
			return False
		ret = self.remove_snapshot(snap_dev)
		if ret != None:
			print ret
			return False
		target.clear()
		path='/root/workspace/FVM/data/target'
		WriteFile(path, target)
		return True

	def SendMessage(self, addr, port, msg):
		print addr, port
		sock = socket.socket()
		sock.connect((addr,port))
		msgservice = MsgService()
		msgservice.sendmsg(sock, msg)
		sock.close()

	def RecvMessage(self):
		addr = cfg['addr']
		port = int(cfg['port'])
		print addr, port
		sock = socket.socket()
		sock.bind((addr, port))
		sock.listen(5)
		while True:
			sock.settimeout(3)
			connection,_ = sock.accept()
			try:
				#connection.settimeout(10)
				msg = connection.recv(1024)
				print msg
				break
			except socket.timeout:
				print 'time out--------------------------------'
				return None
		sock.close()
		return msg
		
	def UpdataVolume(self):
		msg = 'updata '+cfg['name']
		hostaddr = cfg['hostaddr']
		hostport = int(cfg['hostport'])
		self.SendMessage(hostaddr, hostport, msg)
		ret = self.RecvMessage()
		if ret != 'umounted':
			print 'remote host not responded!'
			return False
		self.DisassembleVolume()
		#Get changed blocks and send the info to host
		dev = target['original_volume']
		snap_dev = target['snap_dev']
		command = 'lvmsync '+snap_dev+' '+dev
		path = '/root/workspace/FVM/data/changedblocks'
		fp = open(path)
		while True:
			blocks = ''
			i = 0
			while i < 100:
				block = fp.readline()
				if len(block) == 0:
					break
				blocks += ' '+block
				i += 1
			if len(block) == 0:
				msg = 'blocks_end '+str(i)+blocks
				self.SendMessage(hostaddr, hostport, msg)
				break
			else:
				msg = 'blocks '+str(i)+blocks
				self.SendMessage(hostaddr, hostport, msg)
		
		size = target['size']
		self.AssembleVolume(dev, size)
		msg = 'updata_finished '+cfg['name']
		self.SendMessage(hostaddr, hostport, msg)
		# ret = self.message()
		# if ret = -1:
		# 	print 'Updata failed\n'
		# self.remove_target()
		# self.remove_snapshot()
		# self.create_snapshot()
		# self.create_target()
		# msg = 'volume updata finished'
		# self.message(host_addr, host_port, msg)

	# def PrintStatus(self):
	# 	print 'original volume: '+self.original_volume
	# 	print 'snapshot volume: '+self.snap_name
	# 	print 'target id:       '+self.target_id
	# 	print 'target name:     '+self.target_name
