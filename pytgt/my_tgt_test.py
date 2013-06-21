from tgt_ctrl import *

def test_tgt():
	print '     test begin     '.center(100,'*')
	tgt = Tgt()
	import random,time
	target_id = str(random.randint(20,30))
	target_name = 'iqn:test'+str(time.time())
	acl = 'ALL'
	lun_index = '1'
	lun_path = '/dev/VolGroup/data'
	path = '/dev/mapper/VolGroup-data'

	# test new target, new lun, bind target
	#tgt.new_target(target_id, target_name)
	#tgt.bind_target(target_id, acl)
	#tgt.new_lun(target_id, lun_path, lun_index)
	tgt.new_lun(27, lun_path, 1)
	#tgt.assemble(target_id, target_name, lun_path)

	# for i in range(20,31):
	# 	target_id = str(i)
	# 	tgt.delete_target(target_id)
	
	tgt.reload()
	tgt.print_out()
	

	print 
	print '     test end     '.center(100,'*')


if __name__=="__main__":
	test_tgt()
	