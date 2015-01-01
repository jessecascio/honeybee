#!/usr/bin/python
import sys, shutil, os, subprocess, fileinput, re, mmap

# ./hive.py generate application <>
# ./hive.py delete application <application>

"""
Grab action
"""
try:
	action = sys.argv[1]
	if action != "harvest" and action != "terminate":
		raise Exception()

	type = sys.argv[2]
	if type != "app" and type != "server":
		raise Exception()

	app_name = sys.argv[3]

	if type == "server":
		server_name = sys.argv[4]

except:
	print "ERROR: Missing arguments \n ./hive.py harvest/terminate app/server **<name(s)>"
	sys.exit(2)

"""
Determine type
"""
if type == "app":
	if action == "harvest":
		try:
			shutil.copytree("src/bootstrap/app", "applications/"+app_name)
		except OSError as e:
			print "ERROR: Unable to create app: " + e.strerror

	if action == "terminate":
		try:
			shutil.rmtree("applications/"+app_name)
		except OSError as e:
			print "ERROR: Unable to remove app: " + e.strerror

if type == "server":
	if os.path.isdir("applications/"+app_name) == False:
		print "ERROR: Application ("+app_name+") does not exist"
		sys.exit(2)

	if action == "harvest":
		try:
			shutil.copytree("src/bootstrap/server/template", "applications/"+app_name+"/servers/"+server_name)
		except OSError as e:
			print "ERROR: Unable to create server: " + e.strerror

		# update configs
		path = "applications/"+app_name+"/servers/"+server_name+"/honeycomb.py"
		subprocess.call("sed -i.tmp 's/%%TEMPLATE_PATH%%/templates\= \ \"servers\/"+server_name+"\/templates\"/g' "+path, shell=True)		
		subprocess.call("sed -i.tmp 's/%%ROLES%%/\@roles\(\""+server_name+"\"\)/g' "+path, shell=True)		
		subprocess.call("rm "+path+".tmp", shell=True)

	if action == "terminate":
		try:
			shutil.rmtree("applications/"+app_name+"/servers/"+server_name)
		except OSError as e:
			print "ERROR: Unable to remove server: " + e.strerror


# update the templates
"""
f = open("applications/simp/fabfile.py", "r+")
lines = f.readlines()
lines.insert(2,"asds\n")
f.truncate(0)         
f.seek(0)
f.writelines(lines)
"""

"""
1) Copy app dir
2) remove the .placeholder files
3) Create a dir in test/
"""
# ./hive.py harvest app <>
# ./hive.py terminate app <>

# ./hive.py harvest server <app> <>
# ./hive.py terminate server <app> <>