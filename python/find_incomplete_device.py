from NetworkManagement.Service.DeviceService import NetworkDeviceService

def get_incomplete_device(devices, location='sh'):
    return [ d for d in devices if (d.sysOid!= 'None' or d.sysOid!='') and (d.model.find('No ')>= 0 or d.model=='None' or d.model=='') and d.location==location ]

def get_sysOid_set(devices):
    sysOid_dict = dict()
    for d in devices:
        if d.sysOid:
            if d.sysOid in sysOid_dict:
                sysOid_dict[d.sysOid].append((d.managementIP, d.name))
            else:
                sysOid_dict[d.sysOid] = [(d.managementIP, d.name)]
        print(sysOid_dict)
    return sysOid_dict

if __name__ == '__main__':

    ds = NetworkDeviceService()
    devices = ds.getAllDevices(known=False)

    devices = get_incomplete_device(devices, location='fz')
    #for d in devices:
    #    print(d.items())

    sysOidSet = get_sysOid_set(devices)
    print(sysOidSet)
