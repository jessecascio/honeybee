from fabric.api import run

def nodejs():
    run('sudo apt-get install nodejs -y')
    run('sudo apt-get install npm -y')
