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

    netStr = ''
    pingCmd = 'ping {ip} -n {repeat} -w 200'
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
    -r              Number of echo requests to send
    -n              Network to test
"""

    def __init__(self):
        self.printUsage()
        
        self.IPs = IP(self.netStr)
        self.__pt.field_names = self.__field_names

    def printUsage(self):
        opts, args = getopt.getopt(sys.argv[1:],"n:r:h",["help"])
        for opt, arg in opts:
            if opt in ['-n']:
                print('net:' + arg)
                self.netStr = arg
            elif "-r" == opt:
                print('repeat:' + arg)
                self.pingCmd = self.pingCmd.format(repeat=arg, ip='{ip}')
            elif opt in ["--help", "-h"]:
                print(self.__USAGE)
                sys.exit(0)
            
    def getIPs(self):
        print(self.IPs.len())
        for ip in self.IPs:
            print(ip)

    def report(self):
        for r in self.result:
            self.__pt.add_row(r)
        print(self.__pt)

    def test(self):
        self.result = []
        tmp_futures = []
        isFinish = False
        for ip in self.IPs:
            tmp_futures.append(self.__executor.submit(os.popen, self.pingCmd.format(ip=ip, repeat=1)))
        while (not isFinish):
            for f in tmp_futures:
                if not f.done():
                    break
            else:
                isFinish = True
            time.sleep(1)
        # print(tmp_futures[0].result().read())
        for idx, ip in enumerate(self.IPs):
            self.result.append(
                (
                    ip, 
                    False if "100% loss" in tmp_futures[idx].result().read() else True
                )
            )
        return self

if __name__ == "__main__":
    # pt = PingTool('172.20.232.0/24')
    pt = PingTool()
    pt.test().report()