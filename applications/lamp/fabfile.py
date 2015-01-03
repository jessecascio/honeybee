from fabric.api import *
from src.utility.common import *
from servers.mysql import honeycomb as mysql
from servers.web import honeycomb as web

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
    'web'   : ['104.236.80.117'],
    'mysql' : ['127.0.0.1:2024']
}

"""
Server private IP addresses
@example env.private['mongo'] = ['10.2.2.4', '192.1.1.10']
"""
env.private = {
	'web'   : ['10.132.238.232'],
    'mysql' : ['10.132.139.57']
}

"""
Tunnel public IP addresses
@example env.tunnel['mongo'] = ['283.23.45.3', '283.23.545.3']
"""
env.tunnel = {
	'mysql' : ['104.236.92.89']
}
