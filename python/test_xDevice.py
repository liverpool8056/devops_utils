from NetworkManagement.Models.networkDevice import xDevice
from NetworkManagement.Service.DeviceService import NetworkDeviceService

if __name__ == '__main__':
    d = xDevice('10.20.101.60')
    d.render()
    print(d.items())
