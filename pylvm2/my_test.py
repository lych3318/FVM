#!/usr/bin/env python
from lvm_ctrl import *

def test_create():
	lvm = LVM2()
	lvm.load()
	lvm.lv_create_snapshot('/dev/mapper/VolGroup-data', 'test_snap1', '50M')
def test_remove():
	lvm = LVM2()
	lvm.load()
	lvm.lv_remove('/dev/mapper/VolGroup-test_snap2')	

if __name__ == '__main__':
	test_create()
	#test_remove()