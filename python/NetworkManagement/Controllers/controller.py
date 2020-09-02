from NetworkManagement.telnet_client import TelnetClient

class LoginError(Exception):
    pass

class DeviceInfoDisMatch(Exception):
    pass

class ConfigError(Exception):
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
        self.managementIP = None
        self.cxt = []

    def __telnet(self, managementIP):
        self.managementIP = managementIP
        tc = TelnetClient(managementIP)
        tc.comm_connect()
        if tc.isConnected() == False:
            raise LoginError('LoginError, cannot login to {managementIP} err_msg is {err_msg}'.format(managementIP=managementIP, err_msg=tc.err_type))
        return tc

    def __ssh(self):
        pass

    def login(self, xDevice):
        if self.isAlive():
            return
        self.channel = self.__telnet(xDevice.managementIP)

    def logoff(self):
        self.channel.close()
        self.channel = None

    def isAlive(self):
        return True if self.channel else False

    def get_raw_name(self):
        return self.channel.get_raw_name()

    def send_cmd(self, cmd):
        self.lastPrompt = self.channel.send_cmd(cmd)
        return self.lastPrompt

    def config_error(self):
        cmd = 'error_cmd'
        self.lastPrompt = self.channel.send_cmd(cmd)

    def get_error_prompt(self):
        self.config_error()
        return self.lastPrompt

class IOSController(Controller):

    #def __init__(self):
    #    super(Controller, self).__init__()

    def checkPromptSuccess(self, cmd, prompt):
        self.isLastCmdSuccess = False if prompt.find('^') >= 0 else True
        try:
            assert self.isLastCmdSuccess == True
        except AssertionError as e:
            err_msg = 'ConfigError, something wrong happened when config for {managementIP}, cmd is: \'{cmd}\'\nprompt is:\n{prompt}'.format(managementIP=self.managementIP, cmd=cmd, prompt=self.lastPrompt)
            self.logoff()
            raise ConfigError(err_msg) from e

    def enable(self, passwd):
        prompt = self.channel.send_cmd('en')
        try:
            assert prompt.strip().endswith(':')
        except AssertionError as e:
            raise EnableError('{host}: unknown enable'.format(host=self.managementIP)) from e 
        prompt = self.channel.send_cmd(passwd)
        try:
            assert prompt.strip().endswith('#')
        except AssertionError as e:
            raise EnableError('{host}: password error'.format(host=self.managementIP)) from e

    def terLen(self):
        cmd = 'ter len 0'
        self.lastPrompt = self.channel.send_cmd(cmd)
        self.checkPromptSuccess(cmd, self.lastPrompt)

    def get_config_syslog(self):
        cmd = 'sh run | in logging'
        self.lastPrompt = self.channel.send_cmd(cmd)
        self.checkPromptSuccess(cmd, self.lastPrompt)
        return self.lastPrompt

    def config_txt(self, lines):
        for cmd in lines:
            self.lastPrompt = self.channel.send_cmd(cmd)
            self.checkPromptSuccess(cmd, self.lastPrompt)
    
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

    #def __init__(self):
    #    super(Controller, self).__init__()

    def terLen(self):
        cmd = 'ter len 0'
        self.lastPrompt = self.channel.send_cmd(cmd)
        self.checkPromptSuccess(cmd, self.lastPrompt)

    def config_txt(self, lines):
        for cmd in lines:
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
        except AssertionError as e:
            err_msg = 'ConfigError, something wrong happened when config for {managementIP}, cmd is: \'{cmd}\'\nprompt is:\n{prompt}'.format(managementIP=self.managementIP, cmd=cmd, prompt=self.lastPrompt)
            self.logoff()
            raise ConfigError(err_msg) from e

class Cisco37Controller(IOSController):

    #def __init__(self):
    #    super(IOSController, self).__init__()
    pass
