from NetworkManagement.Models.networkDevice import xDevice
from NetworkManagement.Service.DeviceService import NetworkDeviceService
from NetworkManagement.utils.redis_conn import redis_conn
from NetworkManagement.telnet_client import TelnetClient

if __name__ == '__main__':
    config_text = ""
    nds = NetworkDeviceService()
    devices = nds.getAllDevices()

    location = 'sh'

    for d in devices:
        if d.location != location or d.isICMPReachable !=True:
            continue
        host_ip = d.managementIP
        tc = TelnetClient(host_ip)
        tc.comm_connect()
        if tc.isConnected():
            print('{name}({ip}) telnet success'.format(name=d.name, ip=d.managementIP))
            tc.close()
            d.telnet_enabled=True
        else:
            print('{name}({ip}) telnet fail, err: {err}'.format(name=d.name, ip=d.managementIP, err=tc.err_type))
            if tc.err_type.find('Connection refused') >= 0 :
                d.telnet_enabled = False
            else:
                d.telnet_enabled = True
        nds.save(d)
