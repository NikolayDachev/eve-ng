#!/usr/bin/env python3
#
# scripts/config_mikrotik.py
#
# Import/Export script for Mikrotik RouterOS.
#
# @author Nikolay Dachev <nikolay@dachev.info>
# @copyright 2022 Nikolay Dachev
# @license BSD-3-Clause
# @link http://www.eve-ng.net/
# @version 20220604 beta

import telnetlib
import multiprocessing
import argparse
import sys
import os
import time
import codecs

class ros_config:
    def __init__(self, args):
        self.conn_timeout = 20
        self.login_timeout = 20
        self.enc = 'ascii'

        self.args = args
        # add '+c' to login user: fix console output
        self.login_user = self.args.user + '+c'

        if self.args.action == "get":
            self.get()
        else:
            self.put()
        sys.exit(0)

    def connect(self):
        tn = telnetlib.Telnet()

        # check if host is alive and telnet port is open
        check_conn_timeout = time.time() + self.conn_timeout
        while True:
            try:
                tn.open(host=self.args.ip, port=self.args.port, timeout=self.args.waitconnect)
                break
            except ConnectionRefusedError as e:
                if time.time() > check_conn_timeout:
                    print("%s after %s seconds" % (e, self.conn_timeout) )
                    tn.close()
                    sys.exit(1)

        check_conn_timeout = time.time() + self.login_timeout
        tn.write(b"\n")
        while True:
            a = tn.expect([br"\.* > ", br'\.*Login:', b"assword: ", b"new password> ", b"\[Y/n\]: "], timeout=2)
            if a[0] == 0:
                # we are login
                tn.write(b"\n")
                break
            elif a[0] == 1:
                # send username 
                tn.write(self.login_user.encode(self.enc) + b"\n")
            elif a[0] == 2:
                # send password
                tn.write(self.args.password.encode(self.enc) + b"\n")
            elif a[0] == 3:
                # send control + c
                tn.write(b"\x03")
            elif a[0] == 4:
                # send n (accept license) 
                tn.write(b"n\r\n")
            elif a[0] == -1:
                continue
            else:
                if time.time() > check_conn_timeout:
                   print("ERROR: Faile to get Console prompt after %s seconds" % self.login_timeout)
                   tn.close()
                   sys.exit(1)
        tn.write(b"\n")
        return tn

    def get(self):
        tn = self.connect()

        # export config
        tn.write(b"/export\r\n")
        time.sleep(3)
        cfg = tn.read_very_eager().decode(self.enc)
        tn.write(b"/quit\r\n")
        tn.close()

        # wrtie config to file
        cfg = (cfg.split('\n'))

        # remove evrething before first comment line (terminalls  bug in 6.49*)
        el_count = 0
        for i in cfg:
            if '#' in i:
                first_element = el_count
                break
            else:
                el_count = el_count + 1

        with open(self.args.file, 'w') as fp:
            for i in cfg[el_count:-1]:
                fp.write(i)
        
        print("INFO: config is exported to %s" % self.args.file)
    
    def put(self):
        # Check if config file exist
        if not os.path.exists(self.args.file):
            print("ERROR: config file '%s' dont exist" % self.args.file)
            sys.exit(1)

        # Remove lock file
        lock = '%s/.lock' %(os.path.dirname(self.args.file))
        if os.path.exists(lock):
            os.remove(lock)

        # Mark as configured
        configured = '%s/.configured' %(os.path.dirname(self.args.file))
        if not os.path.exists(configured):
            open(configured, 'a').close()

        # reset configuration
        tn = self.connect()

        tn.write(b"/system reset-configuration no-defaults=yes\r\n")
        time.sleep(3)
        tn.write(b'y\r\n')
        tn.close()

        # put new config
        config_rsc = ''
        time.sleep(3)
        
        tn = self.connect()

        with open(self.args.file, 'r') as fp:
            config_rsc = fp.read().splitlines()

        for cmd in config_rsc:
            if cmd == '':
                continue
            tn.write(cmd.encode(self.enc) + b"\r\n")
            time.sleep(0.1)

        time.sleep(3)
        tn.write(b"/quit\r\n")
        tn.close()
        
        print("INFO: '%s' configuration is applayed" % self.args.file)
    
def arguments():
    parser = argparse.ArgumentParser(description='Configure Mirktoik RouterOS eve-ng',
                                     formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-a','--action', choices=['get', 'put'], type=str,
                        help='''    get: Export startup configuartion and create satrtup-config
    put: Import satrtup-config as startup configuartion''', required=True)
    parser.add_argument('-f','--file', type=str, help='RouterOS configuration file', required=True)
    parser.add_argument('-p','--port', type=int, help='RouterOS telnet port', required=True)
    parser.add_argument('-t','--timeout', type=int, default=30, help='Default operations timeout [default: %(default)s]')
    parser.add_argument('-wc','--waitconnect', type=int, default=20, help='Wait to RouterOS connect timeout [default: %(default)s]')
    parser.add_argument('-i','--ip', type=str, default='127.0.0.1',help='RouterOS IP address [default: %(default)s]')
    parser.add_argument('-u','--user', type=str, default='admin',help='RouterOS login username [default: %(default)s]')
    parser.add_argument('-pwd','--password', type=str, default='',help='RouterOS login password [default: %(default)s]')
    args = parser.parse_args()
    return args

def now():
    ' Return current UNIX time in milliseconds '
    return int(round(time.time() * 1000))

# MAIN
if __name__ == '__main__':
    ros_config(arguments())
    sys.exit(0)
