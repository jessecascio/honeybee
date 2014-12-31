from fabric.api import run

def git():
    run('sudo apt-get install git -y')
    
"""
Clone git code base
"""
def git_clone(url, destination, owner=None, permissions=None):
	"""
	@param string: git url string, git@github.com:symfony/symfony.git
	@param string: project destination, /var/www/symfony
	@param string: owner of project
	@param string: permissions of project

	"""
	# need a tmp git folder
	run('mkdir -p /tmp/honeybee_git')

	run('cd /tmp/honeybee_git && git clone %(url)s'%{'url':url})

	if owner is not None:
		run('sudo chown -R %(owner)s:%(owner)s /tmp/honeybee_git/*'%{'owner':owner})

	if permissions is not None:
		run('sudo chmod -R %(permissions)s /tmp/honeybee_git/*'%{'permissions':permissions})

	run('sudo mv /tmp/honeybee_git/* %(destination)s'%{'destination':destination})