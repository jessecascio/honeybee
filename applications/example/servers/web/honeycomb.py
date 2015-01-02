from fabric.api import *
from os import walk
from src.utility.common import *
from src.ubuntu.apt import *
from src.ubuntu.git import *
from src.ubuntu.apache import *
from src.ubuntu.php import *
from src.ubuntu.hhvm import *
from src.ubuntu.nodejs import *
from src.ubuntu.iptables import *

"""
Commands for this server type
"""

# functions to share
__all__ = ['plant','pollinate','harvest']

# path to template files 
templates = 'servers/web/templates'

# apache user
apache = 'www-data'

@task()
@roles('web')
def plant():
	# enable swap
	swap('2G')
	
	# set up ssh rules
	scp('templates/sshd_config', '/etc/ssh/sshd_config', 'root', '644')
	sudo('service ssh reload')

	# install services
	apt_update()
	git()
	apache2()
	php55()	
	phalcon()
	hhvm()
	nodejs()

	# set default apache configurations
	configure_apache()

	# set the iptables
	iptables_web()

	# pull the code
	git_clone('git@bitbucket.org:jessecascio/jessesnet.com.git','/var/www/jessesnet.com','www-data','750')
	git_clone('git@bitbucket.org:jessecascio/tierralengua.org.git','/var/www/tierralengua.org','www-data','750')
	git_clone('git@bitbucket.org:jessecascio/api.tierralengua.org.git','/var/www/api.tierralengua.org','www-data','750')
	git_clone('git@bitbucket.org:jessecascio/pristinemarketing.com.git','/var/www/pristinemarketing.com','www-data','750')
	git_clone('git@bitbucket.org:jessecascio/apc.jessesnet.com.git','/var/www/apc.jessesnet.com','www-data','750')

	# set up default config files
	sudo('cp /var/www/jessesnet.com/environment.php.default /var/www/jessesnet.com/environment.php')
	sudo('cp /var/www/tierralengua.org/assets/config.default.js /var/www/tierralengua.org/assets/config.js')
	sudo('cp /var/www/api.tierralengua.org/config.php.default /var/www/api.tierralengua.org/config.php')
	sudo('cp /var/www/pristinemarketing.com/environment.php.default /var/www/pristinemarketing.com/environment.php')

	# set the correct apache perms
	apache_perms()

@task()
@roles('web')
def pollinate():
	# move the php config files
	rsync(templates + '/php/', '/etc/php5/mods-available/', 'root', '644')

	# move the apache config files
	scp(templates + '/apache/apache2.conf', '/etc/apache2/apache2.conf', apache)
	scp(templates + '/apache/security.conf', '/etc/apache2/conf-available/security.conf', apache)
	scp(templates + '/apache/mpm_prefork.conf', '/etc/apache2/mods-available/mpm_prefork.conf', apache)

	# move the vhosts and enable them
	rsync(templates + '/apache/vhosts/', '/etc/apache2/sites-available/', apache, '644')

	# enable all the vhost files
	for (dirpath, dirnames, filenames) in walk(templates+'/apache/vhosts/'):
	    for file in filenames:
	    	sudo('a2ensite %(file)s'%{'file':file})

	# reload server
	sudo('service apache2 reload')

@task()
@roles('web')
def harvest():
	pass

"""
Set the default Apache configurations
"""
def configure_apache():
	# disable modules
	sudo('a2dismod env')
	sudo('a2dismod negotiation')
	sudo('a2dismod status')

	# enable modules
	sudo('a2enmod headers')
	sudo('a2enmod rewrite')

	# disable the default vhost
	sudo('a2dissite 000-default.conf')

	# remove html folder
	sudo('rm -rf /var/www/html')
	
	# restart server
	sudo('service apache2 restart')

	# add user to apache group
	sudo('usermod -a -G %(apache)s %(user)s'%{'apache':apache,'user':env.user})

"""
Set the correct perms on the apache dir
"""
def apache_perms():
	sudo('chown -R %(apache)s:%(apache)s /var/www'%{'apache':apache})
	sudo('chmod -R 750 /var/www')
