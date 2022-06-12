This script do export/import Mikrotik RouterOS configuratin for EVE-NG   

Tested with:   

- 6.39, 6.48.6
- 6.49, 6.49.5, 6.49.6, 6.49rc2
- 7.21, 7.2.3
- 7.3beta40, 7.3.1
- 7.4beta2

(11 nodes): cpu:1/ram:256mb per node   
(eve-ng): 5.0.1-11 (cpu:2/ram:16g) vm  

How to use:

```
# make a backup
cp /opt/unetlab/scripts/config_mikrotik.py /opt/unetlab/scripts/config_mikrotik.py.org

# overwirte the original script
cp ./scripts/config_mikrotik.py /opt/unetlab/scripts/config_mikrotik.py
```

NOTES: 
- Please be sure your eve-ng node is up and running before do configuration export.   
- Script will auto set eve-ng node to login prompt before do configuration export.   
  `login with 'admin+c' is needed in order to do proper export.  `
- General process timeout is replaced with per operation timeout(make more sencse for some situation like low node ram or over all eve-ng overload cause node slower boot!).  
  `after every restart the script will close the current connection and reconnect to terminal.`  
  `timeout if the script not able to connect to terminal.`  
  `timeout if the script not get login prompt.`  
- multiprocessing is complicated with class as process, if is really needed all functions can be set and used without class (more var's work will be needed)!  

