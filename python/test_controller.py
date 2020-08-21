from NetworkManagement.Controllers.controller import ControllerFactory
from NetworkManagement.Models.networkDevice import xDevice

d = xDevice('10.29.100.201', telnet_enabled=True)
controllerFactory = ControllerFactory()
c37Controller = controllerFactory.get_controller('CISCO37')
c37Controller.login(d)
print(c37Controller.get_raw_name())
c37Controller.terLen()
c37Controller.config_syslog()
print(c37Controller.lastPrompt)
print(c37Controller.isLastCmdSuccess)
#c37Controller.ip_arp()
