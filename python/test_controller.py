from NetworkManagement.Controllers.controller import ControllerFactory
from NetworkManagement.Models.networkDevice import xDevice

controllerFactory = ControllerFactory()

#d = xDevice('10.20.102.100', telnet_enabled=True)
#iosController = controllerFactory.get_controller('IOS')
#iosController.login(d)
#print(iosController.get_raw_name())
#iosController.terLen()
#iosController.get_config_syslog()
#print(iosController.lastPrompt)
#print(iosController.isLastCmdSuccess)
#c37Controller.ip_arp()

d = xDevice('10.20.101.210', telnet_enabled=True)
nxController = controllerFactory.get_controller('Nexus')
nxController.login(d)
print(nxController.get_raw_name())
nxController.terLen()
#print(nxController.get_error_prompt())
print(nxController.get_config_syslog())
nxController.logoff()
