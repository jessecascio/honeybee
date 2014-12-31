from fabric.api import *
from src.utility.common import *
from servers.web import honeycomb as web
from servers.database import honeycomb as database

# beekeeper web.plant:host=10.2.2.2 --user=vagrant
# ssh -f jesse@104.236.79.221 -L 2024:104.236.73.146:22 -N

# prevents command line override, defaults to user running fab
env.user = 'jesse'

# load config into env.
config_reader('config/config.ini')

# code path
code_path = '/var/www'

# server ips
env.roledefs = {
    'web'      : ['73.293.48.34'],
    'database' : ['127.0.0.1:2024']
}

# private ips
env.private = {
	'web'     : ['10.136.145.34'],
	'database': ['10.163.153.59']
}


