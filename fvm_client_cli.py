# import argparse
# from fvm_client import *

# parser = argparse.ArgumentParser(prog = 'fvm', description='Process FVM client command')
# subparsers = parser.add_subparsers(help='client sub-command help')

# parser_config = subparsers.add_parser('config', help='config')
# parser_config.add_argument('--addr', type=str, help='ip address')
# parser_config.add_argument('--port', type=int, help='port', default='5921')
# parser_config.add_argument('--name', type=str, help='name')
# parser_config.set_defaults(func='config')

# parser_register = subparsers.add_parser('register', help='get remote volume')
# parser_register.add_argument('--addr', type=str, help='remote user name')
# parser_register.add_argument('--port', type=str, help='remote user address', default='5921')
# parser_register.set_defaults(func='register')

# parser_updata = subparsers.add_parser('updata', help='updata volume')
# parser_updata.set_defaults(func='updata')

# parser_assemble = subparsers.add_parser('assemble', help='assemble volume')
# parser_assemble.set_defaults(func='assemble')

# parser_disassemble = subparsers.add_parser('disassemble', help='disassemble volume')
# parser_disassemble.set_defaults(func='disassemble')

# args = parser.parse_args()
# print args.func
# print args

# fvmclient = FVMClient()
# if args.func == 'config':
# 	fvmclient.config(args.addr, args.port, args.name)
# if args.func == 'register':
# 	fvmclient.register()
# if args.func == 'updata':
# 	fvmclient.VolumeUpdata()
# if args.func == 'assemble':
# 	fvmclient.AssembleVolume()
# if args.func == 'disassemble':
# 	fvmclient.DisassembleVolume()

import cmd
import argparse
from fvm_client import *
#from fvm_host_backend import *

fvmclient = FVMClient()

def ParseCMD(action, command):
	#print command, action

	parser = argparse.ArgumentParser(prog = 'fvm', description='Process FVM host command')
	parser.add_argument('--addr', type=str, help='ip address')
	parser.add_argument('--port', type=str, help='port', default='5921')
	parser.add_argument('--name', type=str, help='name')
	#remote host configuration
	parser.add_argument('--hostaddr', type=str, help='host ip address')
	parser.add_argument('--hostport', type=str, default='5921', help='ip address')
	#assemble volume parameters
	parser.add_argument('--volume', type=str, help='original volume')
	#parser.add_argument('--volname', type=str, help='host ip address')
	parser.add_argument('--size', type=str, default='20', help='snap volume size')

	args = parser.parse_args(command.split())
	#print type(args)

	arglist = []
	if action=='config':
		fvmclient.config(args.addr, args.port, args.name, args.hostaddr, args.hostport)
	elif action=='register':
		fvmclient.register()
	elif action=='assemble':
		fvmclient.AssembleVolume(args.volume, args.size)
	elif action=='disassemble':
		fvmclient.DisassembleVolume()
	# elif action=='status':
	# 	fvmclient.PrintStatus()

class FVMCmd(cmd.Cmd):
	"docstring for fvmcmd"
	def do_config(self, line):
		ParseCMD('config', line)

	def do_register(self, line):
		ParseCMD('register', line)

	def do_updata(self, line):
		ParseCMD('updata', line)

	def do_assemble(self, line):
		ParseCMD('assemble', line)

	def do_disassemble(self, line):
		ParseCMD('disassemble', line)

	def do_exit(self, line):
		exit(1)

if __name__ == '__main__':
	fvmcmd = FVMCmd()
	fvmcmd.cmdloop()