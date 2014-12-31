from fabric.api import run

def apt_update():
    run('sudo apt-get update -y')
    