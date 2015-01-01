from fabric.api import *
from src.utility.common import *

# load config inti env.
config('config/config.ini')

# server ips
env.roledefs = {
    'server' : ['']
}

# private ips
env.private = {
	'server' : ['']
}
