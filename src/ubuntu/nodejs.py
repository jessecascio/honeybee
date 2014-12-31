from fabric.api import sudo

def nodejs():
    sudo('apt-get install nodejs -y')
    sudo('apt-get install npm -y')
