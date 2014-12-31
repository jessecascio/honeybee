from fabric.api import run,env,local,sudo
import ConfigParser

"""
Common functionality used across all applications
"""

"""
Copy a local file to the server
"""
def scp(template, destination, owner=None, permissions=None):
	"""
	@param string: path to local template file, EX: templates/sshd_config.conf
	@param string: absolute path to location on server, EX: /etc/ssh/sshd_config/conf
	@param string: owner of file
	@param string: permissions of file
	"""
	# copy and move the file
	local('scp -P %(port)s %(template)s %(user)s@%(host)s:/tmp/honeybee_tmp_file'%{'template':template,'host':env.host ,'port':env.port,'user':env.user})
	sudo('mv /tmp/honeybee_tmp_file %(destination)s'%{'destination':destination})

	# update owner/perms
	if owner is not None:
		sudo('chown %(owner)s:%(owner)s %(destination)s'%{'destination':destination,'owner':owner})

	if permissions is not None:
		sudo('chmod %(permissions)s %(destination)s'%{'destination':destination,'permissions':permissions})

"""
Copy a local directory, or a directory's files to server
"""
def rsync(dir, destination, owner=None, permissions=None):
	"""
	@param string: path to local dir to copy, trailing / just files, no trailing the whole dir
	@param string: absolute path to location on server, will retain same file name
	@param string: owner of files
	@param string: permissions of files
	"""
	# need a tmp rsync folder
	sudo('mkdir -p /tmp/honeybee_rsync')
	sudo('chown %(user)s:%(user)s /tmp/honeybee_rsync'%{'user':env.user})

	local("rsync -avz --rsh='ssh -p%(port)s' %(dir)s %(user)s@%(host)s:/tmp/honeybee_rsync/"%{'dir':dir,'host':env.host,'port':env.port,'user':env.user})

	# update owner/perms
	if owner is not None:
		sudo('chown -R %(owner)s:%(owner)s /tmp/honeybee_rsync/*'%{'owner':owner})

	if permissions is not None:
		sudo('chmod -R %(permissions)s /tmp/honeybee_rsync/*'%{'permissions':permissions})

	# move the files
	sudo('mv /tmp/honeybee_rsync/* %(destination)s'%{'destination':destination})

	# clean up
	sudo('rm -rf /tmp/honeybee_rsync')

"""
Create an ssh tunnel
"""	
def tunnel(ip,port,remote_ip,remote_port=22):
	"""
	@param string: IP of server forwarding from i.e. web server
	@param string: local port to attach tunnel to
	@param string: IP of server tunneling to i.e. db server
	@param string: port to attach to on remote server
	"""
	# update to be an array: port => remote_ip
	local('ssh -f %(user)s@%(ip)s -L %(port)s:%(remote_ip)s:%(remote_port)s -N'%{'user':env.user,'ip':ip,'port':port,'remote_ip':remote_ip,'remote_port':remote_port})

"""
Delete port tunnel
"""	
def detunnel(port):
	local('fuser -k -n tcp %(port)s'%{'port':port})

"""
Set up swap
"""	
def swap(size):
	"""
	@param string: swap size, 4G, 256M, etc
	"""
	# set up swap
	sudo('fallocate -l %(size)s /swapfile'%{'size':size})
	sudo('chmod 600 /swapfile')
	sudo('mkswap /swapfile')
	sudo('swapon /swapfile')
	# configure
	sudo('sysctl vm.swappiness=10')
	sudo('sysctl vm.vfs_cache_pressure=50')
	# make permenant
	run('echo "vm.swappiness=10" | sudo tee -a /etc/sysctl.conf')
	run('echo "vm.vfs_cache_pressure=50" | sudo tee -a /etc/sysctl.conf')
	run('echo "/swapfile   none    swap    sw    0   0" | sudo tee -a /etc/fstab')

"""
Reads an .ini config file and assignes values to env global dict
Uses format, env.section_option, no spaces
"""
def config(config):
	"""
	@param string: path to local config file
	"""
	Config = ConfigParser.ConfigParser()
	Config.read(config)

	dict1 = {}

	for section in Config.sections():
		for option in Config.options(section):
			env[section.replace(" ","")+"_"+option.replace(" ","")] = Config.get(section, option)


