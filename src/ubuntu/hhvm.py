from fabric.api import run

def hhvm():
    run('wget -O - http://dl.hhvm.com/conf/hhvm.gpg.key | sudo apt-key add -')
    run('echo deb http://dl.hhvm.com/ubuntu trusty main | sudo tee /etc/apt/sources.list.d/hhvm.list')
    run('sudo apt-get update -y')
    run('sudo apt-get install hhvm -y')
    