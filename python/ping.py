import os
from IPy import IP
import pprint
import prettytable
from concurrent.futures import ThreadPoolExecutor
import time

class PingTool:

    netStr = ''
    pingCmd = 'ping %s -n 1 -w 200'
    IPs = None
    result = []
    __field_names = ['IP', 'isReachable']
    __pt = prettytable.PrettyTable()
    __executor = ThreadPoolExecutor(256)


    def __init__(self, netStr):
        self.netStr = netStr
        self.IPs = IP(netStr)
        self.__pt.field_names = self.__field_names

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
            tmp_futures.append(self.__executor.submit(os.popen, self.pingCmd%ip))
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
    pt = PingTool('172.20.160.0/23')
    pt.test().report()