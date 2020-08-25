from NetworkManagement.Service.DeviceService import NetworkDeviceService
from NetworkManagement.Controllers.controller import ControllerFactory
from NetworkManagement.Models.networkDevice import xDevice

if __name__ == '__main__':
    nds = NetworkDeviceService()
    devices = nds.getAllDevices()
    #telnet
    #devices = [ d for d in devices if d.telnet_enabled ]
    #sysOid
    #sysOid = 'SNMPv2-SMI::mib-2.47.1.1.1.1.2.2'
    #devices = [ d for d in devices if d.sysOid==sysOid]
    #manufacturer
    manufacturer = 'Cisco'
    devices = [ d for d in devices if d.manufacturer.find(manufacturer)>=0 ]
    #model exclude
    #model_patterns = ['N3', 'N5', 'N7', 'N9', 'No Such', 'ASR', 'ISR']
    #for model_pattern in model_patterns:
    #    devices = [ d for d in devices if d.model.find(model_pattern)<0 or d.model == '' ]
    #model include
    model = 'N5'
    devices = [ d for d in devices if d.model.find(model) >= 0 or d.model == '' ]
    #location
    location = 'sh'
    devices = [ d for d in devices if d.location==location ]
    #zone exclude
    #zones = ['YuanGongWang', 'DianHua', 'ShiTang']
    #devices = [ d for d in devices if d.zone not in zones ]
    #zone include
    zone = 'JiaoYi'
    devices = [ d for d in devices if d.zone==zone ]
    print(len(devices))

    for d in devices:
        print('model:{model}, manufacturer: {manufacturer}'.format(model=d.model, manufacturer=d.manufacturer))
    
    controllerFactory = ControllerFactory()
    controller = controllerFactory.get_controller('Nexus')

    for d in devices:
        print('Login to {device}'.format(device=d.managementIP))
        try:
            controller.login(d)
        except:
            print('Fail to login')
            continue
        print(controller.get_raw_name())
        controller.terLen()
        config_syslog = controller.get_config_syslog()
        print(config_syslog)
        controller.logoff() 
