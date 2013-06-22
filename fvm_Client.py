from pylvm2.lvm_ctrl import *
import iscsi.scandev

def FVMClient():
	def __init__(self):
		self.lvm = LVM2()
		self.lvm.load()
		self.tgt = Tgt()
		pass

	def create_snapshot(original_dev, snap_name, size):
		self.lvm.lv_create_snapshot(original_dev, snap_name, size)

	def remove_snapshot(dev):
		self.lvm.lv_remove(dev)

	def create_target(target_id, target_name, lun_dev):
		acl = 'all'
		lun_index = '1'
		self.tgt.new_target(target_id, target_name)
		self.tgt.bind_target(target_id, acl)
		self.tgt.new_lun(target_id, lun_path, lun_index)

	def remove_target(target_name):
		target_id = self.tgt.target_name2target_id(target_name)
		if target_id == None:
			print 'No such target'
			return
		if self.tgt.delete_target(target_id) != None:
			print 'failed to Disassemble Volume' + target_name

	def assemble_volume():
		pass

	def message():
		pass
