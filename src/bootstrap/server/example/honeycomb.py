from fabric.api import *
from src.utility.common import *

"""
Commands for this server type
"""

# functions to share
__all__ = ['plant','pollinate','harvest']

# path to template files
%%TEMPLATE_PATH%%

@task()
%%ROLES%%
def plant():
	pass

@task()
%%ROLES%%
def pollinate():
	pass

@task()
%%ROLES%%
def harvest():
	pass
