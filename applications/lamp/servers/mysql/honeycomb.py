from fabric.api import *
from src.utility.common import *
from src.ubuntu.apt import *
from src.ubuntu.mysql import *
from src.ubuntu.iptables import *

"""
Commands for this server type
"""

# functions to share
__all__ = ['plant','pollinate','harvest']

# path to template files
templates=  "servers/mysql/templates"

@task()
@roles('mysql')
def plant():
	web_pub   = env.roledefs['web'][0]
	web_pri   = env.private['web'][0] 
	mysql_tun = env.tunnel['mysql'][0]

	# (1) set up tunnel info
	tunnel(web_pub, '2024', mysql_tun)

	# add swap
	swap('2G')

	# set up ssh rules
	scp('templates/sshd_config', '/etc/ssh/sshd_config', 'root', '644')
	sudo('service ssh reload')

	# (2) install services
	apt_update()
	mysql56(env.database_password)	

	# (3) default db/users
	run('mysql -uroot -p%(pwd)s -e "CREATE DATABASE datahouse"'%{'pwd':env.database_password})
	run('mysql -uroot -p%(pwd)s -e "CREATE USER \'rick\'@\'%(ip)s\' IDENTIFIED BY \'supersecret\'"'%{'pwd':env.database_password,'ip':web_pri})
	run('mysql -uroot -p%(pwd)s -e "GRANT ALL PRIVILEGES ON datahouse.* TO \'rick\'@\'%(ip)s\'"'%{'pwd':env.database_password,'ip':web_pri})
	run('mysql -uroot -p%(pwd)s -e "FLUSH PRIVILEGES"'%{'pwd':env.database_password})

	# (4) default db settings
	scp(templates + '/my.cnf', '/etc/mysql/my.cnf', 'root', '644')
	sudo('service mysql restart')

	# (5) build allowable ips to access server, set iptables
	ips = env.roledefs['web'] + env.private['web']
	iptables_database(ips)

	# (6) kill tunnel
	detunnel('2024')

@task()
@roles("mysql")
def pollinate():
	web_pub   = env.roledefs['web'][0]
	mysql_tun = env.tunnel['mysql'][0]

	# set up tunnel info
	tunnel(web_pub, '2024', mysql_tun)

	# reload the conf file
	scp(templates + '/my.cnf', '/etc/mysql/my.cnf', 'root', '644')
	sudo('service mysql reload')

	# kill tunnel
	detunnel('2024')

@task()
@roles("mysql")
def harvest():
	pass
