from fabric.api import run

def apache2():
    run('sudo apt-get install apache2 -y')
