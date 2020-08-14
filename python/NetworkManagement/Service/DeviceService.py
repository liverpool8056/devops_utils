from NetworkManagement.utils.redis_conn import redis_conn
from NetworkManagement.snmp import NDCollector
from NetworkManagement.Models.networkDevice import xDevice
pingSrc = '10.20.97.100'
ip_key_pattern = 'ip:{ip}'

class NetworkDeviceService:

    def __init__(self):
        self.redis_conn = redis_conn
    
    def getDeviceByZone(self, zone):
        devices = []
        device_keys = self.__getDeviceKeys()
        for key in device_keys:
            device_obj = self.redis_conn.hgetall(key)
            ip_zone = ip_obj.get('zone', '')
            if ip_zone == zone:
                ips.append(ip_obj)
        return ips

    def getDeviceBySysOid(self, sysoid):
        devices = []
        device_keys = self.__getDeviceKeys()
        for key in device_keys:
            device_obj = self.redis_conn.hgetall(key)
            sysOid = device_obj.get('sysOid', '')
            if sysOid != sysoid:
                continue
            if 'managementIP' in device_obj.keys():
                man_ip = device_obj['managementIP']
            else:
                man_ip = device_obj['ip']
                device_obj.update(dict(managementIP=man_ip))
                del device_obj['ip']
            devices.append(xDevice(**device_obj))
        return devices

    def getAllDevices(self):
        devices = []
        # filter device which is snmpUnreachable
        device_keys = [ key for key in self.__getKeys() if not key.endswith(':') ]
        for key in device_keys:
            device_obj = self.redis_conn.hgetall(key)
            #sysOid = device_obj.get('sysOid', '')
            #if len(sysOid)==0:
                #continue
            if 'managementIP' in device_obj.keys():
                man_ip = device_obj['managementIP']
            else:
                man_ip = device_obj['ip']
                device_obj.update(dict(managementIP=man_ip))
                del device_obj['ip']
            devices.append(xDevice(**device_obj))
        return devices

    def getDeviceByIP(self, managementIP):
        device_keys = self.redis_conn.keys('networkDevice:'+managementIP+':*')
        assert len(device_keys) == 0
        return self.redis_conn.hgetall(device_keys[0])

    def isExist(self, xDevice):
        return True if self.__getDeviceKeys(xDevice) else False

    def delIfExist(self, xDevice):
        keys = self.__getDeviceKeys(xDevice)
        print(f'delete keys: [{keys}]')
        for key in keys:
            self.redis_conn.delete(key)

    def save(self, xDevice):
        key_pattern = 'networkDevice:{ip}:{name}'
        self.delIfExist(xDevice)
        key = key_pattern.format(ip=xDevice.managementIP, name=xDevice.name)
        self.redis_conn.hmset(key, xDevice.to_redis_value())
    
    def login(self, xDevice):
        host_ip = xDevice.managementIP
        host_channel = Channel(host_ip)
        return host_channel

    def __getDeviceKeys(self, xDevice):
        key = 'networkDevice:{ip}:*'.format(ip=xDevice.managementIP)
        keys = self.redis_conn.keys(key)
        return keys

    def __getKeys(self):
        return self.redis_conn.keys('networkDevice:*')

if __name__ == '__main__':
    zone = 'M'
    print(NetworkDeviceService.getIPByZone(zone))
