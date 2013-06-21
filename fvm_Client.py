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

	def create_target():
		pass

	def remove_target():
		pass
