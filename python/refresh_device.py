from NetworkManagement.Service.DeviceService import NetworkDeviceService

if __name__ == '__main__':
    ds = NetworkDeviceService()
    devices = ds.getAllDevices(known=False)
    location = 'sh'
    devices = [d for d in devices if d.managementIP.startswith('10.20.100.')]
    for d in devices:
        d.zone = 'YuanGongWang'
        ds.save(d)
