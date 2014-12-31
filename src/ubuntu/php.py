from fabric.api import sudo

def php55():
    sudo('apt-get install php5 php5-common php5-cli php5-mysql php5-memcached php5-curl php5-mongo php5-apcu -y')
    composer()
    phpunit()
    
def phalcon():
	sudo('apt-add-repository ppa:phalcon/stable -y')
	sudo('apt-get update -y')
	sudo('apt-get install php5-phalcon -y')

def composer():
	sudo('curl -sS https://getcomposer.org/installer | sudo php -- --install-dir=/tmp')
	sudo('mv /tmp/composer.phar /usr/local/bin/composer')
	sudo('chmod +x /usr/local/bin/composer')
    
def phpunit():
	sudo('wget https://phar.phpunit.de/phpunit.phar')
	sudo('chmod +x phpunit.phar')
	sudo('mv phpunit.phar /usr/local/bin/phpunit')
	