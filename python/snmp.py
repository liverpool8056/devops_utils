import os
from IPy import IP
import pprint
import prettytable
from concurrent.futures import ThreadPoolExecutor
import time
import getopt
import sys
import argparse
import sys

class PingTool:

    PING_CMD_SET = {
        'win32': 'ping {ip} -n {repeat} -w 200',
        'darwin': 'ping {ip} -c {repeat} -w 200',
        'linux': 'ping {ip} -c {repeat} -w 1'
    }
    PING_CMD = PING_CMD_SET[sys.platform]
    UNREACHABLE_STRING_SET = {
        'win32': '100% loss',
        'darwin': '100.0% packet loss',
        'linux': '100% packet loss'
    }
    UNREACHABLE_STRING = UNREACHABLE_STRING_SET[sys.platform]
    repeat = 1
    state = 'all'
    netStr = ''

    IPs = None
    result = []
    __field_names = ['IP', 'isReachable']
    __pt = prettytable.PrettyTable()
    __executor = ThreadPoolExecutor(256)
    __USAGE = """
PingTool is used to ping all host ip in a specified netwok, and can display a report

Usage: python ping.py [-n] [-r count] [-n net]

Options:
    -h,--help       Print usage
    -c              Count of ping requests to be sent
    -n              Network to test
    -s              return a subset of ip list. True is for reachable ip, false is for unreachable 
"""

    def __init__(self):
        self.parser_cli()
        self.print_args()
        
        self.IPs = IP(self.netStr)
        self.__pt.field_names = self.__field_names

    def parser_cli(self):
        if len(sys.argv) < 2:
            print(self.__USAGE)
            sys.exit(0)
        opts, args = getopt.getopt(sys.argv[1:],"n:c:s:h",["help"])
        for opt, arg in opts:
            if opt in ['-n']:
                self.netStr = arg
            elif "-c" == opt:
                self.repeat = arg
                self.pingCmd = self.PING_CMD.format(repeat=arg, ip='{ip}')
            elif "-s" == opt:
                if arg == 'true':
                    self.state = True
                elif arg == 'false':
                    self.state = False
                else:
                    print(self.__USAGE)
                    sys.exit(0)
            elif opt in ["--help", "-h"]:
                print(self.__USAGE)
                sys.exit(0)

    def print_args(self):
        tmp = ''
        tmp += 'count: %s\t'%self.repeat
        tmp += 'network: %s\t'%self.netStr
        tmp += 'state: %s'%self.state
        print(tmp)
            
    def getIPs(self):
        print(self.IPs.len())
        for ip in self.IPs:
            print(ip)

    def report(self, state='all'):
        for r in self.result:
            self.__pt.add_row(r)
        print(self.__pt)

    def filter(self):
        if self.state != 'all':
            self.result = [ r for r in self.result if r[-1]==self.state ]
        return self

    def probe(self):
        self.result = []
        tmp_futures = []
        isFinish = False
        for ip in self.IPs:
            tmp_futures.append(self.__executor.submit(os.popen, self.pingCmd.format(ip=ip, repeat=self.repeat)))
        while (not isFinish):
            for f in tmp_futures:
                if not f.done():
                    break
            else:
                isFinish = True
            time.sleep(1)
        for idx, ip in enumerate(self.IPs):
            self.result.append(
                (
                    ip, 
                    False if self.UNREACHABLE_STRING in tmp_futures[idx].result().read() else True
                )
            )
        return self

if __name__ == "__main__":
    pt = PingTool()
    pt.probe().filter().report()
    executor = ThreadPoolExecutor(256)
    snmp_cmd = "snmpwalk -v 2c -c xyzqnetmanager {ip} SNMPv2-MIB::sysName.0"
    for ip, state in pt.result:
        tmp_futures.append(executor.submit(os.popen, snmp_cmd.format(ip=ip)))
    isFinish = False
    while (not isFinish):
        for f in tmp_futures:
            if not f.done():
                break
        else:
            isFinish = True
        time.sleep(1)
    for idx, ip in 
