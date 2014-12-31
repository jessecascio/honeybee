from fabric.api import sudo

def apt_update():
    sudo('apt-get update -y')
    