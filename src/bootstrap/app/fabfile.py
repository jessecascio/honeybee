from fabric.api import *
from src.utility.common import *
from servers.web import honeycomb as web

env.user = 'vagrant'

# load config inti env.
config_reader('config/config.ini')

env.roledefs = {
    'web'      : ['10.2.2.2'],
    'database' : ['10.2.2.4']
}
