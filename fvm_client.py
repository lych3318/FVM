from pylvm2.lvm_ctrl import *
import iscsi.scandev

class FVMClient():
	def __init__(self):
		self.lvm = LVM2()
		self.lvm.load()
		self.tgt = Tgt()

	def load(self, config_file):
		pass

	def config(self, addr, port, name):
		FVMClient.addr = addr
		FVMClient.port = port
		FVMClient.name = name

	def register(self, host_addr, host_port=5921):
		msg = 'register '+self.name+' '+self.addr+' '+self.port
		self.message(host_addr, host_port, msg)

	def create_snapshot(self, original_dev, snap_name, size):
		self.lvm.lv_create_snapshot(original_dev, snap_name, size)

	def remove_snapshot(self, dev):
		self.lvm.lv_remove(dev)

	def create_target(self, target_id, target_name, lun_dev):
		acl = 'all'
		lun_index = '1'
		self.tgt.new_target(target_id, target_name)
		self.tgt.bind_target(target_id, acl)
		self.tgt.new_lun(target_id, lun_path, lun_index)

	def remove_target(self, target_name):
		target_id = self.tgt.target_name2target_id(target_name)
		if target_id == None:
			print 'No such target'
			return
		if self.tgt.delete_target(target_id) != None:
			print 'failed to Disassemble Volume' + target_name

	def AssembleVolume(self, self, dev):
		self.create_snapshot(dev, xx, xx)
		self.create_target(xx, xx, xx)
		self.message()

	def DisassembleVolume(self):
		self.remove_target()
		self.remove_snapshot()
		self.message()

	def SendMessage(self, addr, port, msg):
		sock = socket.socket()
		sock.connect((addr,port))
		msgservice = MsgService()
		msgservice.sendmsg(sock, msg)

	def VolumeUpdata(self):
		msg = 'volume updata start'
		self.message(host_addr, host_port, msg)
		# ret = self.message()
		# if ret = -1:
		# 	print 'Updata failed\n'
		self.remove_target()
		self.remove_snapshot()
		self.create_snapshot()
		self.create_target()
		msg = 'volume updata finished'
		self.message(host_addr, host_port, msg)

