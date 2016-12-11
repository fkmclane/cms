import argparse
import signal


from cms import config


parser = argparse.ArgumentParser(description='serve up a content management system for markdown files')
parser.add_argument('-a', '--address', dest='address', help='address to bind')
parser.add_argument('-p', '--port', dest='port', help='port to bind')
parser.add_argument('-t', '--template', dest='template', help='template directory to use')
parser.add_argument('-l', '--log', dest='log', help='log directory to use')
parser.add_argument('root', nargs='?', help='root directory to serve markdown files')

args = parser.parse_args()

if args.address:
    config.addr = (args.address, config.addr[1])

if args.port:
    config.addr = (config.addr[0], args.port)

if args.template:
    config.template = args.template

if args.log:
    if args.log == 'none':
        config.log = None
        config.httplog = None
    else:
        config.log = args.log + '/cms.log'
        config.httplog = args.log + '/http.log'

if args.root:
    config.root = args.root


from cms import name, version
from cms import log, http


log.cmslog.info(name + ' ' + version + ' starting...')

# start everything
http.start()


# cleanup function
def exit():
    http.stop()


# use the function for both SIGINT and SIGTERM
for sig in signal.SIGINT, signal.SIGTERM:
    signal.signal(sig, exit)
