from fabric.api import run

def mongodb():
	# get key, create list
	run('sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 7F0CEB10')
	run("echo 'deb http://downloads-distro.mongodb.org/repo/ubuntu-upstart dist 10gen' | sudo tee /etc/apt/sources.list.d/mongodb.list")
	# update OS, install
	run('sudo apt-get update -y')
	run('sudo apt-get install -y mongodb-org')

    