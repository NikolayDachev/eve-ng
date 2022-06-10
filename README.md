This script do export/import Mikrotik RouterOS configuratin for EVE-NG   

Testing with:   

- 6.39, 6.48.6
- 6.49, 6.49.5, 6.49.6, 6.49rc2
- 7.21, 7.2.3, 7.3beta40

Script is still in development   

How to use:

```
# make a backup
cp /opt/unetlab/scripts/config_mikrotik.py /opt/unetlab/scripts/config_mikrotik.py.org

# overwirte the original script
cp ./scripts/config_mikrotik.py /opt/unetlab/scripts/config_mikrotik.py
```

NOTE: 
- Please be sure your eve-ng node is up and running before do configuration export.   
- Script will auto set eve-ng node to login prompt before do configuration export.   
  login with 'admin+c' is needed in order to do proper export.

TODO:
- check multiiprocesing
- testing