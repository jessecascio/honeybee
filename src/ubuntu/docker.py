from fabric.api import sudo

def docker():
	sudo('curl -sSL https://get.docker.com/ | sh')
    