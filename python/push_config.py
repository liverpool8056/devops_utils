from NetworkManagement.Controllers.controller import ControllerFactory
from NetworkManagement.Service.DeviceService import NetworkDeviceService

def push_config(iplist):
    nds = NetworkDeviceService()
    controllerFactory = ControllerFactory()
    for ip in iplist:
        device = nds.getDeviceByIP(ip)
        print(device.items())
    
if __name__ == '__main__':

    ips = [
        '10.20.101.60',
        '10.20.101.70',
        '10.20.101.110',
        '10.20.101.140',
        '10.20.101.210',
        '10.20.101.211',
        '10.20.101.212',
        '10.20.101.213',
        '10.20.101.214',
        '10.20.101.215',
        '10.20.101.216',
        '10.20.101.217',
        '10.20.101.218',
        '10.20.101.219',
        '10.20.101.220',
        '10.20.101.221',
        '10.20.101.222',
        '10.20.101.223',
        '10.20.101.224',
        '10.20.101.225',
        '10.20.101.226',
        '10.20.101.227',
        '10.20.101.228',
        '10.20.101.229',
        '10.20.101.230',
        '10.20.101.231',
        '10.20.101.232',
        '10.20.101.233',
        '10.20.101.234',
        '10.20.101.235',
        '10.20.101.236',
        '10.20.101.237',
        #'10.26.2.12', #N5K
        #'10.26.2.13'  #N5K
    ]

    push_config(ips)
