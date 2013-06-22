import argparse

parser = argparse.ArgumentParser(prog = 'fvm', description='Process FVM host command')
subparsers = parser.add_subparsers(help='sub-command help')

parser_config = subparsers.add_parser('config', help='config')
parser_config.add_argument('addr', type=str, help='ip address')
parser_config.add_argument('port', type=int, help='port')
parser_config.add_argument('name', type=str, help='name')

parser_get = subparsers.add_parser('get', help='get remote volume')
parser_get.add_argument('--name', type=str, help='remote user name')
parser_get.add_argument('--addr', type=str, help='remote user address')

parser_updata = subparsers.add_parser('updata', help='updata remote volume')
parser_updata.add_argument('name', type=str, help='remote user name')
parser_updata.add_argument('addr', type=str, help='remote user address')

parser_umount = subparsers.add_parser('umount', help='get remote volume')
parser_umount.add_argument('name', type=str, help='remote user name')
parser_umount.add_argument('addr', type=str, help='remote user address')

args = parser.parse_args()
print args