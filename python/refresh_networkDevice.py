from NetworkManagement.Models.networkDevice import xDevice
from NetworkManagement.Service.DeviceService import NetworkDeviceService

if __name__ == '__main__':
    #sysOid = 'SNMPv2-SMI::enterprises.9.1.1041'
    #sysOid = 'SNMPv2-SMI::enterprises.9.12.3.1.3.1410'
    #sysOid = 'SNMPv2-SMI::enterprises.9.12.3.1.3.1238'
    #sysOid = 'SNMPv2-SMI::enterprises.9.1.1707'
    #sysOid = 'SNMPv2-SMI::enterprises.9.12.3.1.3.1812'
    #sysOid = 'SNMPv2-SMI::enterprises.9.1.1644'
    #sysOid = 'SNMPv2-SMI::enterprises.9.12.3.1.3.1354'
    #sysOid = 'SNMPv2-SMI::enterprises.9.1.1643'
    nds = NetworkDeviceService()
    devices = nds.getAllDevices()
    for d in devices:
        d.render()
        nds.save(d)
        print(d)
