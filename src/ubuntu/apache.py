from fabric.api import sudo

def apache2():
    sudo('apt-get install apache2 -y')
