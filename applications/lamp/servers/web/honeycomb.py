from fabric.api import *
from os import walk
from src.utility.common import *
from src.ubuntu.apt import *
from src.ubuntu.git import *
from src.ubuntu.apache import *
from src.ubuntu.php import *
from src.ubuntu.iptables import *

"""
Commands for this server type
"""

# functions to share
__all__ = ['plant','pollinate','harvest']

# path to template files
templates=  "servers/web/templates"

@task()
@roles("web")
def plant():
	# enable swap
	swap('2G')
	
	# (2) set up ssh rules
	scp('templates/sshd_config', '/etc/ssh/sshd_config', 'root', '644')
	sudo('service ssh reload')
	
	# (3) set the iptables
	iptables_web()

	# (4) install services
 	apt_update()
	git()
	apache2()
	php55()	
	
	# (5) set default apache configurations
	sudo('a2dismod status')
	sudo('a2enmod headers')
	sudo('a2enmod rewrite')
	sudo('service apache2 restart')
	
	# (6) pull code
	git_clone('git@github.com:symfony/symfony.git','/var/www/symfony','www-data','750')

@task()
@roles('web')
def pollinate():
	# (1) set up the php config files
	rsync(templates + '/php/', '/etc/php5/mods-available/', 'root', '644')

	# (2) set up the apache config files
	scp(templates + '/apache/apache2.conf', '/etc/apache2/apache2.conf', 'www-data')
	scp(templates + '/apache/security.conf', '/etc/apache2/conf-available/security.conf', 'www-data')
	scp(templates + '/apache/mpm_prefork.conf', '/etc/apache2/mods-available/mpm_prefork.conf', 'www-data')

	# (3) move the vhosts and enable them
	rsync(templates + '/apache/vhosts/', '/etc/apache2/sites-available/', 'www-data', '644')

	for (dirpath, dirnames, filenames) in walk(templates+'/apache/vhosts/'):
	    for file in filenames:
	    	sudo('a2ensite %(file)s'%{'file':file})

	# (4) reload server
	sudo('service apache2 reload')

@task()
@roles("web")
def harvest():
	pass
