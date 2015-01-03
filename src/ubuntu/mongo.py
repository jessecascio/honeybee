from fabric.api import run,sudo

def mongodb():
	# get key, create list
	sudo('apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 7F0CEB10')
	run("echo 'deb http://downloads-distro.mongodb.org/repo/ubuntu-upstart dist 10gen' | sudo tee /etc/apt/sources.list.d/mongodb.list")
	# update OS, install
	sudo('apt-get update -y')
	sudo('apt-get install -y mongodb-org')

    