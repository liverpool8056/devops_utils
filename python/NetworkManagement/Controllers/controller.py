from NetworkManagement.telnet_client import TelnetClient

class LoginError(Exception):
    pass

class DeviceInfoDisMatch(Exception):
    pass

class ControllerFactory:

    def __init__(self):
        pass

    def get_controller(self, crtlr_type):
        if crtlr_type == 'CISCO37':
            return Cisco37Controller()
        if crtlr_type == 'IOS':
            return IOSController()
        if crtlr_type == 'Nexus':
            return NexusController()

class Controller:

    def __init__(self):
        self.channel = None
        self.isLastCmdSuccess = False
        self.lastPrompt = None
        self.cxt = []

    def __telnet(self, managementIP):
        tc = TelnetClient(managementIP)
        tc.comm_connect()
        if tc.isConnected() == False:
            raise LoginError('LoginError, err_msg is {err_msg}'.format(err_msg=tc.err_type))
        return tc

    def __ssh(self):
        pass

    def login(self, xDevice):
        #if xDevice.telnet_enabled:
        self.channel = self.__telnet(xDevice.managementIP)
        #print('login success')

    def logoff(self):
        self.channel.close()

    def isAlive(self):
        return True if self.channel else False

    def get_raw_name(self):
        return self.channel.get_raw_name()

    def config_error(self):
        cmd = 'error_cmd'
        self.lastPrompt = self.channel.send_cmd(cmd)

    def get_error_prompt(self):
        self.config_error()
        return self.lastPrompt

class IOSController(Controller):

    def __init__(self):
        super(Controller, self).__init__()

    def checkPromptSuccess(self, cmd, prompt):
        self.isLastCmdSuccess = False if prompt.find('^') >= 0 else True
        try:
            assert self.isLastCmdSuccess == True
        except AssertionError:
            err_msg = 'ConfigError, cmd is {cmd}, prompt is {prompt}'.format(cmd=line, prompt=self.lastPrompt)
            raise ConfigError(err_msg)

    def terLen(self):
        cmd = 'ter len 0'
        self.lastPrompt = self.channel.send_cmd(cmd)
        self.checkPromptSuccess(cmd, self.lastPrompt)

    def get_config_syslog(self):
        cmd = 'sh run | in logging'
        self.lastPrompt = self.channel.send_cmd(cmd)
        self.checkPromptSuccess(cmd, self.lastPrompt)
        return self.lastPrompt

    def config_syslog(self):
        config_txt = [
        "conf t",
        "logg trap warnings",
        "logging source-interface vlan666",
        "logging host 129.25.98.33",
        "exit",
        "wr"
        ]
        for cmd in config_txt:
            self.lastPrompt = self.channel.send_cmd(cmd)
            self.checkPromptSuccess(cmd, self.lastPrompt)

    def ip_arp(self):
        cmd = 'sh ip arp'
        self.lastPrompt = self.channel.send_cmd(cmd)
        self.isLastCmdSuccess = self.checkPromptSuccess(cmd, self.lastPrompt)
        print(self.lastPrompt)

class NexusController(Controller):

    def __init__(self):
        super(Controller, self).__init__()

    def terLen(self):
        cmd = 'ter len 0'
        self.lastPrompt = self.channel.send_cmd(cmd)
        self.checkPromptSuccess(cmd, self.lastPrompt)

    def get_config_syslog(self):
        cmd = 'sh run | in logging'
        self.lastPrompt = self.channel.send_cmd(cmd)
        self.checkPromptSuccess(cmd, self.lastPrompt)
        return self.lastPrompt

    def checkPromptSuccess(self, cmd, prompt):
        self.isLastCmdSuccess = False if prompt.find('^') >= 0 else True
        try:
            assert self.isLastCmdSuccess == True
        except AssertionError:
            err_msg = 'ConfigError, cmd is {cmd}, prompt is {prompt}'.format(cmd=line, prompt=self.lastPrompt)
            raise ConfigError(err_msg)

class Cisco37Controller(IOSController):

    def __init__(self):
        super(IOSController, self).__init__()
