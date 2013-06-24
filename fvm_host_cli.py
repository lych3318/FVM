import cmd
import argparse
#from fvm_host_backend import *

cfg = {}

def ParseCMD(action, command):
	print command, action

	parser = argparse.ArgumentParser(prog = 'fvm', description='Process FVM host command')
	parser.add_argument('--addr', type=str, help='ip address')
	parser.add_argument('--port', type=str, help='port', default='5921')
	parser.add_argument('--name', type=str, help='name')
	parser.add_argument('--root', type=str, help='root directory')

	args = parser.parse_args(command.split())
	print type(args)

	if action=='config':
		cfg['addr']=args.addr
		cfg['port']=args.port
		cfg['name']=args.name
		cfg['root']=args.root
		print cfg
	else:
		DoAction()


	#subparsers = parser.add_subparsers(help='sub-command help')

	# parser_config = subparsers.add_parser('config', help='config')
	# parser_config.add_argument('--addr', type=str, help='ip address')
	# parser_config.add_argument('--port', type=int, help='port', default='5921')
	# parser_config.add_argument('--name', type=str, help='name')
	# parser_config.set_defaults(func='config')

	# parser_get = subparsers.add_parser('get', help='get remote volume')
	# parser_get.add_argument('--name', type=str, help='remote user name')
	# parser_get.add_argument('--addr', type=str, help='remote user address')
	# parser_get.set_defaults(func='get')

	# parser_updata = subparsers.add_parser('updata', help='updata remote volume')
	# parser_updata.add_argument('--name', type=str, help='remote user name')
	# parser_updata.add_argument('--addr', type=str, help='remote user address')
	# parser_updata.set_defaults(func='updata')

	# parser_umount = subparsers.add_parser('umount', help='get remote volume')
	# parser_umount.add_argument('--name', type=str, help='remote user name')
	# parser_umount.add_argument('--addr', type=str, help='remote user address')
	# parser_umount.set_defaults(func='umount')

	# args = parser.parse_args(command.split())
	# print args.func
	# print args

class FVMCmd(cmd.Cmd):
	"docstring for fvmcmd"
	def do_config(self, line):
		ParseCMD('config', line)

	def do_mount(self, line):
		ParseCMD('mount', line)

	def do_updata(self, line):
		ParseCMD('updata', line)

	def do_umount(self, line):
		ParseCMD('umount', line)

	def do_exit(self, line):
		exit(1)

if __name__ == '__main__':
	fvmcmd = FVMCmd()
	fvmcmd.cmdloop()