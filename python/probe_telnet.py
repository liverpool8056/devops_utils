from NetworkManagement.Models.networkDevice import xDevice
from NetworkManagement.Service.DeviceService import NetworkDeviceService
from NetworkManagement.utils.redis_conn import redis_conn
from NetworkManagement.telnet_client import TelnetClient
from NetworkManagement.ping import PingTool

if __name__ == '__main__':
    config_text = ""
    deviceIPs = [
        '10.20.101.60',
        '10.20.101.70',
        '10.20.101.110',
        '10.20.101.140',
        '10.20.101.223',
        '10.20.101.224',
        '10.20.101.226'
    ]

    nds = NetworkDeviceService()
    #devices = nds.getAllDevices()
    devices = [ xDevice(ip, location='sh', zone='JiaoYi', manufacturer='Cisco') for ip in deviceIPs ]

    location = 'sh'

    for d in devices:
        #if d.location != location or d.isICMPReachable !=True:
        if d.location != location:
            continue
        host_ip = d.managementIP
        tc = TelnetClient(host_ip)
        tc.comm_connect()
        if tc.isConnected():
            name = tc.get_raw_name()
            d.name = name
            print('{name}({ip}) telnet success'.format(name=d.name, ip=d.managementIP))
            tc.close()
            d.telnet_enabled=True
        else:
            print('{name}({ip}) telnet fail, err: {err}'.format(name='', ip=d.managementIP, err=tc.err_type))
            if tc.err_type.find('Connection refused') >= 0 :
                d.telnet_enabled = False
            else:
                d.telnet_enabled = True
        nds.save(d)
