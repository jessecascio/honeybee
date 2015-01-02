from fabric.api import *
from src.utility.common import *
from src.ubuntu.apt import *
from src.ubuntu.mysql import *
from src.ubuntu.mongo import *
from src.ubuntu.iptables import *

"""
Commands for this server type
"""

# functions to share
__all__ = ['plant','pollinate','harvest']

# path to template files
templates = 'servers/database/templates'

# ip for db server, used with tunnel
# @TODO incorportate into env.
db_server = '104.236.79.221'
db_port   = '2024'

@task()
@roles('database')
def plant():
	# set up tunnel info
	tunnel(env.roledefs['web'][0], db_port, db_server)

	# add swap
	swap('2G')

	# set up ssh rules
	scp('templates/sshd_config', '/etc/ssh/sshd_config', 'root', '644')
	sudo('service ssh reload')

	# install services
	apt_update()
	mysql56(env.database_password)	
	mongodb()

	# create users
	mysql_users()

	# set default db configurations
	configure_db()

	# build allowable ips to access server, set iptables
	ips = env.roledefs['web'] + env.private['web']
	iptables_database(ips)

	# kill tunnel
	detunnel(db_port)

@task()
@roles('database')
def pollinate():
	pass

@task()
@roles('database')
def harvest():
	pass

"""
Set the default MySQL configurations
"""
def configure_db():
	# copy the config files
	scp(templates + '/mysql/my.cnf', '/etc/mysql/my.cnf', 'root', '644')
	scp(templates + '/mongo/mongod.conf', '/etc/mongod.conf', 'root', '644')

	# restart servers
	sudo('service mysql restart')
	sudo('service mongod restart')

"""
Create default MySQL users
"""
def mysql_users():
	ip = env.private['web'][0]
	tierra_usr = 'ti3rr@Es'
	tierra_pwd = 'ti3rr@LenguA?'
	jnet_usr   = 'j3ss3n@t'
	jnet_pwd   = 'Jezze-N$t^'

	# create databases
	run('mysql -uroot -p%(pwd)s -e "CREATE DATABASE tierralengua"'%{'pwd':env.database_password})
	run('mysql -uroot -p%(pwd)s -e "CREATE DATABASE wordpress"'%{'pwd':env.database_password})
	
	# tierralengua user
	run('mysql -uroot -p%(pwd)s -e "CREATE USER \'%(user)s\'@\'%(ip)s\' IDENTIFIED BY \'%(upwd)s\'"'%{'pwd':env.database_password,'user':tierra_usr,'ip':ip,'upwd':tierra_pwd})
	run('mysql -uroot -p%(pwd)s -e "GRANT ALL PRIVILEGES ON tierralengua.* TO \'%(user)s\'@\'%(ip)s\'"'%{'pwd':env.database_password,'user':tierra_usr,'ip':ip})
	
	# jessesnet user
	run('mysql -uroot -p%(pwd)s -e "CREATE USER \'%(user)s\'@\'%(ip)s\' IDENTIFIED BY \'%(upwd)s\'"'%{'pwd':env.database_password,'user':jnet_usr,'ip':ip,'upwd':jnet_pwd})
	run('mysql -uroot -p%(pwd)s -e "GRANT ALL PRIVILEGES ON wordpress.* TO \'%(user)s\'@\'%(ip)s\'"'%{'pwd':env.database_password,'user':jnet_usr,'ip':ip})
	
	# flush
	run('mysql -uroot -p%(pwd)s -e "FLUSH PRIVILEGES"'%{'pwd':env.database_password})
	