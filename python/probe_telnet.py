from NetworkManagement.Models.networkDevice import xDevice
from NetworkManagement.Service.DeviceService import NetworkDeviceService
from NetworkManagement.utils.redis_conn import redis_conn
from NetworkManagement.telnet_client import TelnetClient

if __name__ == '__main__':
    config_text = ""
    nds = NetworkDeviceService()
    devices = nds.getAllDevices()

    location = 'sh'

    print(len(devices))

    for d in devices:
        print(type(d.location), d.location)
        if d.location != location or d.:
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
            if 'Connection refused' in tc.err_type:
                d.telnet_enabled=True
        nds.save(d)
