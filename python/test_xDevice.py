from NetworkManagement.Models.networkDevice import xDevice
from NetworkManagement.Service.DeviceService import NetworkDeviceService
from NetworkManagement.utils.redis_conn import redis_conn

if __name__ == '__main__':
    config_text = ""
    nds = NetworkDeviceService()
    devices = nds.getAllDevices()
    for d in devices:
        channel = NetworkDeviceService.login(d)
        channel.config_syslog()
        channel.raw_config(config_text)
