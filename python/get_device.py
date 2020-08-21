#import datetime
from NetworkManagement.Service.DeviceService import NetworkDeviceService
from NetworkManagement.Models.networkDevice import *

if __name__ == '__main__':
    nds = NetworkDeviceService()
    devices = nds.getAllDevices()
    #telnet
    #devices = [ d for d in devices if d.telnet_enabled ]
    #sysOid
    sysOid = 'SNMPv2-SMI::mib-2.47.1.1.1.1.2.2'
    print(devices[0].sysOid)
    devices = [ d for d in devices if d.sysOid==sysOid]
    for d in devices:
        print(d.items())
