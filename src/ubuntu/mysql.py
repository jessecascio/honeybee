from fabric.api import run
import pipes

def mysql56(password):
	"""
	@param string: default mysql password
	"""
	# escape for command line
	password = pipes.quote(password)

	# disable interactive mode
	run('echo "mysql-server-5.6 mysql-server/root_password password %(pwd)s" | sudo debconf-set-selections'%{'pwd':password})
	run('echo "mysql-server-5.6 mysql-server/root_password_again password %(pwd)s" | sudo debconf-set-selections'%{'pwd':password})
	
	# install server
	run('sudo apt-get install mysql-server-5.6 -y')

	# security updates
	run('mysql -uroot -p%(pwd)s -e "DELETE FROM mysql.user WHERE User=\'\'"'%{'pwd':password})
	run('mysql -uroot -p%(pwd)s -e "DELETE FROM mysql.user WHERE User=\'root\' AND Host NOT IN (\'localhost\', \'127.0.0.1\', \'::1\')"'%{'pwd':password})
	run('mysql -uroot -p%(pwd)s -e "DROP DATABASE IF EXISTS test"'%{'pwd':password})
	run('mysql -uroot -p%(pwd)s -e "FLUSH PRIVILEGES"'%{'pwd':password})

    