This script do export/import Mikrotik RouterOS configuratin for EVE-NG   

Tested with:   

- 6.39, 6.48.6
- 6.49, 6.49.5, 6.49.6, 6.49rc2, 6.49.6  
- 7.21, 7.2.3
- 7.3beta40, 7.3.1
- 7.4beta2
- 7.6

(11 nodes): cpu:1/ram:256mb per node   
(eve-ng): 5.0.1-11 (cpu:2/ram:16g) vm  

- export all cfg
- start all nodes with startup-confg
- per node
- ...

How to use:

```
# make a backup
cp /opt/unetlab/scripts/config_mikrotik.py /opt/unetlab/scripts/config_mikrotik.py.org

# overwirte the original script
cp ./scripts/config_mikrotik.py /opt/unetlab/scripts/config_mikrotik.py
```

This script support several useful options (like set login user/password), however they can be used only via eve-ng node shell (not via web ui)

```
/opt/unetlab/scripts/config_mikrotik.py --help
usage: config_mikrotik.py [-h] -a {get,put} -f FILE -p PORT [-t TIMEOUT] [-wc WAITCONNECT] [-i IP] [-u USER] [-pwd PASSWORD] [-lr LOGIN_RETRIES] [-fr FORCE_ADMIN_PWD_RESET]

Configure Mirktoik RouterOS eve-ng

optional arguments:
  -h, --help            show this help message and exit
  -a {get,put}, --action {get,put}
                            get: Export startup configuartion and create satrtup-config
                            put: Import satrtup-config as startup configuartion
  -f FILE, --file FILE  RouterOS configuration file
  -p PORT, --port PORT  RouterOS telnet port
  -t TIMEOUT, --timeout TIMEOUT
                        Default operations timeout [default: 30]
  -wc WAITCONNECT, --waitconnect WAITCONNECT
                        RouterOS connect interval [default: 20]
  -i IP, --ip IP        RouterOS IP address [default: 127.0.0.1]
  -u USER, --user USER  RouterOS login username [default: admin]
  -pwd PASSWORD, --password PASSWORD
                        RouterOS login password [default: ]
  -lr LOGIN_RETRIES, --login-retries LOGIN_RETRIES
                        Number of max login retries [default: 3]
  -fr FORCE_ADMIN_PWD_RESET, --force-admin-pwd-reset FORCE_ADMIN_PWD_RESET
                        Force admin password reset [default: False]

```

First you should find [LAB_ID] and [NODE_ID] via EVE-NG ui  

[LAB_ID] -> left panel -> Lab Details  
[NODE_ID] -> left panel -> Nodes  

examples cli usage:

Import Startup-Config  

```
cmd:
/opt/unetlab/scripts/config_mikrotik.py -a put -p 32769 -f /opt/unetlab/tmp/0/[LAB_ID]]/[NODE_ID]/startup-config -t 300

example:
/opt/unetlab/scripts/config_mikrotik.py -a put -p 32769 -f /opt/unetlab/tmp/0/9665d2a8-1fa2-4a36-82fa-1dcaa3f38e5a/1/startup-config -t 300 
INFO: '/opt/unetlab/tmp/0/9665d2a8-1fa2-4a36-82fa-1dcaa3f38e5a/1/startup-config' configuration is applayed
```

Export Startup-Config  
```
TODO
```


NOTES: 
- Please be sure you did NOT set `admin` user passsword via init setup, import script or configuration.  
  If ros is setup via winbox just cancel `new password` prompt, if is via ros cli just cancel it with `ctl+c`  
  This script use `admin` user login via telnet(terminal) in order to make import/export .  
  If password is set the script will fail to login and will not be able to make export
  NOTE: If you see this error just restart ros node and remove `admin` with `/user/set admin password=""`!  
- Please be sure your eve-ng node is up and running before do configuration export.   
- Script will auto set eve-ng node to login prompt before do configuration export.   
  `login with 'admin+c' is needed in order to do proper export.  `
- General process timeout is replaced with per operation timeout(make more sencse for some situation like low node ram or over all eve-ng overload cause node slower boot!).  
  `after every restart the script will close the current connection and reconnect to terminal.`  
  `timeout if the script not able to connect to terminal.`  
  `timeout if the script not get login prompt.`  
- multiprocessing is complicated with class as process, if is really needed all functions can be set and used without class (more var's work will be needed)!  

