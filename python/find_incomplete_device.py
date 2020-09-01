from NetworkManagement.Service.DeviceService import NetworkDeviceService

def get_incomplete_device(devices):
    return [ d for d in devices if d.sysOid!= 'None' and d.model.find('No ')>= 0 and d.location=='sh' ]

def get_sysOid_set(devices):
    sysOid_set = set()
    for d in devices:
        if d.sysOid:
            sysOid_set.add(d.sysOid)
    return sysOid_set

if __name__ == '__main__':

    ds = NetworkDeviceService()
    devices = ds.getAllDevices(known=False)

    devices = get_incomplete_device(devices)
    for d in devices:
        print(d.items())

    #sysOidSet = get_sysOid_set(devices)
    #print(sysOidSet)
