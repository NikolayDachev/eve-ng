This script do export/import Mikrotik RouterOS configuratin for EVE-NG   

```
This script is not official!
I developed it since current eve-ng (community ed.) is broken and cannot do proper statup-config import/export.
I really hope eve-ng team will fix the official eve-ng (comm ed.) script.
```

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

