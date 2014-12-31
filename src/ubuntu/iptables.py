from fabric.api import run,sudo

"""
Ubuntu IP table rules
"""

"""
Save IP tables
"""
def iptables_save():
	sudo('iptables-save')

"""
Reset IP tables
"""
def iptables_reset():
	# reset so we dont lose session
	sudo('iptables -P OUTPUT ACCEPT')
	sudo('iptables -P INPUT ACCEPT')
	sudo('iptables -P FORWARD ACCEPT')

	sudo('iptables -F')

"""
Enforce IP tables
"""
def iptables_enforce():
	# drop anything not specified
	sudo('iptables -P OUTPUT ACCEPT')
	sudo('iptables -P INPUT DROP')
	sudo('iptables -P FORWARD DROP')

	# save and restart
	iptables_save()
	sudo('service ufw restart')

"""
Common IP table rules
"""
def iptables_common():
	# stop common attacks
	sudo('iptables -A OUTPUT -p icmp --icmp-type 8 -j DROP')
	sudo('iptables -A INPUT -p tcp --tcp-flags ALL NONE -j DROP')
	sudo('iptables -A INPUT -p tcp --tcp-flags ALL ALL -j DROP')
	sudo('iptables -A INPUT -f -j DROP')
	sudo('iptables -A INPUT -p tcp ! --syn -m state --state NEW -j DROP')
	
"""
Set iptable rules for local loopback
"""
def iptables_local():
	# enable local loopback
	sudo('iptables -I INPUT 1 -i lo -j ACCEPT')
	sudo('iptables -A OUTPUT -o lo -j ACCEPT')

"""
Web server IP table rules
"""
def iptables_web():
	iptables_reset()
	iptables_common()
	iptables_local()

	# enable local loopback
	sudo('iptables -I INPUT 1 -i lo -j ACCEPT')
	sudo('iptables -A OUTPUT -o lo -j ACCEPT')

	# open web ports, ssh, git
	sudo('iptables -A INPUT -p tcp --dport 80 -m state --state NEW,ESTABLISHED -j ACCEPT')
	sudo('iptables -A OUTPUT -p tcp --sport 80 -m state --state NEW,ESTABLISHED -j ACCEPT')
	sudo('iptables -A INPUT -p tcp --dport 443 -m state --state NEW,ESTABLISHED -j ACCEPT')
	sudo('iptables -A OUTPUT -p tcp --sport 443 -m state --state NEW,ESTABLISHED -j ACCEPT')
	sudo('iptables -A INPUT -p tcp --dport 22 -m state --state NEW,ESTABLISHED -j ACCEPT')
	sudo('iptables -A OUTPUT -p tcp --sport 22 -m state --state NEW,ESTABLISHED -j ACCEPT')
	sudo('iptables -A INPUT -p tcp --dport 9418 -m state --state NEW,ESTABLISHED -j ACCEPT')
	sudo('iptables -A OUTPUT -p tcp --sport 9418 -m state --state NEW,ESTABLISHED -j ACCEPT')

	# support conntrack
	# http://superuser.com/questions/828198/iptables-on-debian-blocking-git-pull-http-api-requests-etc
	sudo('iptables -A INPUT -m conntrack --ctstate RELATED,ESTABLISHED -j ACCEPT')
	# sudo('iptables -A OUTPUT -m conntrack --ctstate RELATED,ESTABLISHED -j ACCEPT')
	# sudo('iptables -A INPUT -4 -p icmp -j ACCEPT')

	iptables_enforce()

"""
Database server IP table rules
"""
def iptables_database(hosts):
	"""
	@param dict: colletion of web server ip addresses
	"""
	iptables_reset()
	iptables_local()

	# open ssh, mysql, mongo but only to web servers
	for ip in hosts:
		sudo('iptables -A INPUT -p tcp -s %(ip)s --dport 22 -m state --state NEW,ESTABLISHED -j ACCEPT'%{'ip':ip})
		sudo('iptables -A OUTPUT -p tcp --sport 22 -m state --state NEW,ESTABLISHED -j ACCEPT')
		sudo('iptables -A INPUT -p tcp -s %(ip)s --dport 3306 -m state --state NEW,ESTABLISHED -j ACCEPT'%{'ip':ip})
		sudo('iptables -A OUTPUT -p tcp --sport 3306 -m state --state NEW,ESTABLISHED -j ACCEPT')
		sudo('iptables -A INPUT -p tcp -s %(ip)s --dport 27017 -m state --state NEW,ESTABLISHED -j ACCEPT'%{'ip':ip})
		sudo('iptables -A OUTPUT -p tcp --sport 27017 -m state --state NEW,ESTABLISHED -j ACCEPT')

	iptables_enforce()
