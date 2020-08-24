import datetime
from NetworkManagement.Service.DeviceService import NetworkDeviceService
DIR = '/opt/tools/python/out/'
ts = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
fname = f'devices.{ts}.csv'

def output_csv(devices):
    with open(DIR+fname, 'w') as f_handler:
        if len(devices):
            th = devices[0].items().keys()
            f_handler.write(','.join(th)+'\n')
            for d in devices:
                row = [d.items().get(h, '').replace(',', '.') for h in th]
                f_handler.write(','.join(row)+'\n')

if __name__ == '__main__':

    nds = NetworkDeviceService()
    devices = nds.getAllDevices()
    rows = []
    
    #telnet
    #devices = [ d for d in devices if d.telnet_enabled ]
    #location:fz
    devices = [ d for d in devices if d.location=='fz' ]
    
    output_csv(devices)
