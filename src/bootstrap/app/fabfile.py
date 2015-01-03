from fabric.api import *
from src.utility.common import *

"""
EXAMPLE

beekeeper web.plant --user=swift
beekeeper web.pollinate --user=swift
beekeeper web.harvest --user=swift
"""

# load config inti env.
config('config/config.ini')

"""
Server IP addresses
@example env.roledefs['mongo'] = ['283.23.45.3', '127.0.0.1:2024]
"""
env.roledefs = {
    'server' : ['']
}

"""
Server private IP addresses
@example env.private['mongo'] = ['10.2.2.4', '192.1.1.10']
"""
env.private = {
	'server' : ['']
}

"""
Tunnel public IP addresses
@example env.tunnel['mongo'] = ['283.23.45.3', '283.23.545.3']
"""
env.tunnel = {
	'server' : ['']
}