from NetworkManagement.Service.DeviceService import NetworkDeviceService
from NetworkManagement.Service.ConfigService import ConfigService
from NetworkManagement.Controllers.controller import ControllerFactory
from NetworkManagement.Controllers.controller import LoginError
from NetworkManagement.Controllers.controller import ConfigError
from NetworkManagement.Models.deviceConfig import DeviceConfig

if __name__ == '__main__':
    ds = NetworkDeviceService()
    cs = ConfigService()
    controllerFactory = ControllerFactory()
    devices = ds.getAllDevices(known=False)
    location = 'sh'
    devices = [d for d in devices if d.model.startswith('WS') and d.managementIP.startswith('10.20.100.') and d.location=='sh']
    controller_type = 'IOS'
    for d in devices:
        controller = controllerFactory.get_controller(controller_type)
        if d.managementIP != '10.20.100.150':
            continue
        try:
            if not controller.login(d):
                print('---------------{host} pass-------------'.format(host=d.managementIP))
                print(d.items())
                config = DeviceConfig(owner=d.managementIP, value='telnet_disable')
            else:
                config = controller.get_config_all()
        except (LoginError, ConfigError) as e:
            print('---------------{host} pass-------------'.format(host=d.managementIP))
            print(str(e))
            config = DeviceConfig(owner=d.managementIP, value=str(e))
        cs.save(config)
        #config = cs.get(d)
        #print(config.value)
        print('----------------{host} ok-----------------'.format(host=d.managementIP))
