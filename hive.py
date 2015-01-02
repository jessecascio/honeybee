#!/usr/bin/python
import sys,shutil,os,subprocess

"""
EXAMPLES

./hive.py flower app <>
./hive.py flower server <app> <>
./hive.py exterminate app <>
./hive.py exterminate server <app> <>
"""

"""
Grab command line args
"""
try:
	action = sys.argv[1]
	if action != "flower" and action != "exterminate":
		raise Exception()

	type = sys.argv[2]
	if type != "app" and type != "server":
		raise Exception()

	app_name = sys.argv[3]
	if sys.argv[3].isalpha() != True:
		print "App name must contain only letters"
		sys.exit(2)

	if type == "server":
		server_name = sys.argv[4]
		if server_name.isalpha() != True:
			print "Server name must contain only letters"
			sys.exit(2)

except Exception as e:
	print "ERROR: Missing arguments \n ./hive.py flower/exterminate app/server **<name(s)>"
	sys.exit(2)

"""
Do work
"""
if type == "app":
	if action == "flower":
		# copy folders
		try:
			shutil.copytree("src/bootstrap/app", "applications/"+app_name)
			shutil.copytree("src/bootstrap/test", "test/"+app_name)
		except OSError as e:
			print "ERROR: Unable to create app: " + e.strerror

		# remove placeholder files
		try:
			os.remove("applications/"+app_name+"/tasks/.placeholder")
			os.remove("applications/"+app_name+"/templates/.placeholder")
		except OSError as e:
			print "ERROR: Unable to clean app: " + e.strerror
				
	if action == "exterminate":
		# verify
		if raw_input("Delete "+app_name+"? [y/n]: ") != "y" :
			sys.exit(2)

		# remove
		try:
			shutil.rmtree("applications/"+app_name)
			shutil.rmtree("test/"+app_name)
		except OSError as e:
			print "ERROR: Unable to remove app: " + e.strerror

if type == "server":
	if os.path.isdir("applications/"+app_name) == False:
		print "ERROR: Application ("+app_name+") does not exist"
		sys.exit(2)

	if action == "flower":
		# move folders
		try:
			shutil.copytree("src/bootstrap/server/example", "applications/"+app_name+"/servers/"+server_name)
		except OSError as e:
			print "ERROR: Unable to create server: " + e.strerror

		# remove tmp files
		try:
			os.remove("applications/"+app_name+"/servers/"+server_name+"/templates/.placeholder")
		except OSError as e:
			print "ERROR: Unable to clean server: " + e.strerror

		# update configs
		path = "applications/"+app_name+"/servers/"+server_name+"/honeycomb.py"
		subprocess.call("sed -i.tmp 's/%%TEMPLATE_PATH%%/templates\= \ \"servers\/"+server_name+"\/templates\"/g' "+path, shell=True)		
		subprocess.call("sed -i.tmp 's/%%ROLES%%/\@roles\(\""+server_name+"\"\)/g' "+path, shell=True)		
		subprocess.call("rm "+path+".tmp", shell=True)

		# import server in fabfile
		fab = open("applications/"+app_name+"/fabfile.py", "r+")
		lines = fab.readlines()
		lines.insert(2,"from servers."+server_name+" import honeycomb as "+server_name+"\n")
		fab.truncate(0)         
		fab.seek(0)
		fab.writelines(lines)

	if action == "exterminate":
		# confirm
		if raw_input("Delete "+server_name+"? [y/n]: ") != "y" :
			sys.exit(2)

		# remove
		try:
			shutil.rmtree("applications/"+app_name+"/servers/"+server_name)
		except OSError as e:
			print "ERROR: Unable to remove server: " + e.strerror

		# remove import from fabfile
		path = "applications/"+app_name+"/fabfile.py"
		subprocess.call("sed -i.tmp 's/from servers\."+server_name+"\ import\ honeycomb\ as\ "+server_name+"//g' "+path, shell=True)		
		subprocess.call("rm "+path+".tmp", shell=True)

