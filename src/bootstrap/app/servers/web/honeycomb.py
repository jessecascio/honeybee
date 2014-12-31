from fabric.api import *
from src.utility.common import *

"""
Commands for this server type
"""

# functions to share
__all__ = ['plant','pollinate','flower']

# path to template files
templates = 'servers/web/templates'

@task()
@roles('web')
def plant():
	pass

@task()
@roles('web')
def pollinate():
	pass

@task()
@roles('web')
def flower():
	pass
