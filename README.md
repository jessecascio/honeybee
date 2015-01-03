Honeybee
===

Honeybee is a templating structure built around the Python Fabric library to organize the shell provisioning of various servers in a cloud cluster.  By setting a standard for where provision commands are stored, and placing installation instructions in centralized locations, Honeybee allows for reusability of installation instructions across various web application servers.  This facilitates rapid, provider agnostic, server provisioning, easy infrastructure expansion, and seamless server migrations.  

See [full tutorial](http://jessesnet.com/portfolio/honeybee-server-provisioning "Honeybee Tutorial").

#### Generating Application Stack

Using the Hive script, define the application stack and add server types

```
./hive.py generate app lamp
./hive.py generate server lamp apache
./hive.py generate server lamp mysql
```

#### Defining Instructions

Use centralized shell commands, wrapped in Python functions, to define server provisioning

```
apache2()
php55()
```

SSH tunnels allow for bypassing advanced firewall rules

```
tunnel('56.23.53.58', '2024', '289.23.57.34')
mysql56()
```

Clean, limited Python Fabric tasks
```
Available commands:

    mysql.harvest
    mysql.plant
    mysql.pollinate
    web.harvest
    web.plant
    web.pollinate

```

Plant, initial server set up, occurs once
```
fab apache.plant
```

Pollinate, push config files to the cluster
```
fab apache.pollinate 
```

Harvest, deploy the application
```
fab apache.deploy
```
