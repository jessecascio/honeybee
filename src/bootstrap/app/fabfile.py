from fabric.api import *
from src.utility.common import *

# load config inti env.
config('config/config.ini')

"""
Server IP Addresses
@example env.roledefs['mongo'] = ['283.23.45.3', '127.0.0.1:2024]
"""
env.roledefs = {
    'server' : ['']
}

"""
Server private IP Addresses
@example env.roledefs['mongo'] = ['10.2.2.4', '192.1.1.10']
"""
env.private = {
	'server' : ['']
}
