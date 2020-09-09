from NetworkManagement.Controllers.controller import ControllerFactory
from NetworkManagement.Service.DeviceService import NetworkDeviceService

def print_resp(host, resp_dict):
    print(f'{host}')
    for cmd in resp_dict:
        resp = resp_dict.get(cmd, 'No Response')
        print(f'\t{cmd}\n\t{resp}')
    print('-'*20)

def get_devices(iplist):
    nds = NetworkDeviceService()
    devices = []
    model_set = set()
    for ip in iplist:
        device = nds.getDeviceByIP(ip)
        model_set.add(device.model)
        devices.append(device)
    print(model_set)
    return devices

def login_devices(devices):
    controllers = []
    controllerFactory = ControllerFactory()
    for d in devices:
        controller_type = 'IOS' if d.model.startswith('WS') else 'Nexus'
        
        controller = controllerFactory.get_controller(controller_type)
        controller.login(d)
        controllers.append(controller)
    return controllers

def logoff_devices(controllers):
    for controller in controllers:
        controller.logoff()
    return controllers

def get_cmd_reps(controller, cmds):
    ret = dict()
    for cmd in cmds:
        resp = controller.send_cmd(cmd)
        ret.update({cmd:resp})
    return ret 

def get_config(controllers):
    for controller in controllers:
        config_syslog = controller.get_config_syslog()
        host = controller.channel.host_info['host']
        print(f'{host}\n\t{config_syslog}')

def filter_devices(devices):
    model = 'WS' # IOS
    return [d for d in devices if d.model.startswith(model)]

def push_config(controllers):
    lines = [
        'conf t',
        #'logging buffered 409600',
        #'logging console emergencies',
        #'hw-switch switch 1 logging onboard message level 3',
        #'logging source-interface Vlan999',
        #'logging server 10.20.97.99',
        #'logging host 10.20.97.99',
        'logging trap warnings',
        'logging source-interface Vlan254',
        'logging 129.25.98.33',
        #'no logging host 10.20.97.99',

        'exit',
        #'copy run start'
        'wr'
    ]
    
    for c in controllers:
        c.config_txt(lines)
        #print(c.lastPrompt)
        #print(c.get_config_syslog())
    
if __name__ == '__main__':

    ips = [
'172.98.254.122'
    ]

    devices = get_devices(ips)
    controllers = login_devices(devices)
    controller = controllers[0]
    controller.enable('xycisco')
    #push_config(controllers)
    get_config(controllers)
    #cmds = ['sh ip int b | in Vlan']
    #for controller in controllers:
    #    resp_dict = get_cmd_reps(controller, cmds)
    #    host = controller.channel.host_info['host']
    #    print_resp(host, resp_dict)
    logoff_devices(controllers)
