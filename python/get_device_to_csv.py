import datetime
from NetworkManagement.Service.DeviceService import NetworkDeviceService
DIR = '/opt/tools/python/out/'
ts = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
fname = f'devices.{ts}.csv'

def output_csv(thead, row):
    with open(fname, 'w') as f_handler:
        f_handler.write(','.join(thead))
        for row in rows:
            f_handler.write(','.join(row))

if __name__ == '__main__':
    th = [
        'name', 
        'managementIP',
        'zone',
        'location',
        'model',
        'version',
        'manufacturer',
    ]

    nds = NetworkDeviceService()
    devices = nds.getAllDevices()
    rows = []
    
    #telnet
    devices = [ d for d in devices if d.telnet_enabled ]
    for d in devices:
        values = []
        values.append(d.name)
        values.append(d.managementIP)
        values.append(d.zone)
        values.append(d.location)
        values.append(d.model)
        values.append(d.version)
        values.append(d.manufacturer)
        rows.append(values)
    
    output_csv(th, rows)
