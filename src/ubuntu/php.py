from fabric.api import run

def php55():
    run('sudo apt-get install php5 php5-common php5-cli php5-mysql php5-memcached php5-curl php5-mongo php5-apcu -y')
    composer()
    phpunit()
    
def phalcon():
	run('sudo apt-add-repository ppa:phalcon/stable -y')
	run('sudo apt-get update -y')
	run('sudo apt-get install php5-phalcon -y')

def composer():
	run('sudo curl -sS https://getcomposer.org/installer | sudo php -- --install-dir=/tmp')
	run('sudo mv /tmp/composer.phar /usr/local/bin/composer')
	run('sudo chmod +x /usr/local/bin/composer')
    
def phpunit():
	run('sudo wget https://phar.phpunit.de/phpunit.phar')
	run('sudo chmod +x phpunit.phar')
	run('sudo mv phpunit.phar /usr/local/bin/phpunit')
	