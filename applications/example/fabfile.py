from fabric.api import *
from src.utility.common import *
from servers.web import honeycomb as web
from servers.database import honeycomb as database

"""
EXAMPLE

beekeeper web.plant --user=swift
beekeeper web.pollinate --user=swift
beekeeper web.harvest --user=swift
"""

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

