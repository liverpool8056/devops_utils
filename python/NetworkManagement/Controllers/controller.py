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

class Controller:

    def __init__(self):
        self.channel = None
        self.isLastCmdSuccess = False
        self.lastPrompt = None
        pass

    def __telnet(self, managementIP):
        tc = TelnetClient(managementIP)
        tc.comm_connect()
        if tc.isConnected() == False:
            raise LoginError('LoginError, err_msg is {err_msg}'.format(err_msg=tc.err_type))
        return tc

    def __ssh(self):
        pass

    def login(self, xDevice):
        if xDevice.telnet_enabled:
            self.channel = self.__telnet(xDevice.managementIP)
        print('login success')

    def isAlive(self):
        return True if self.channel else False

    def get_raw_name(self):
        return self.channel.get_raw_name()

    def logoff(self):
        self.channel.close()

class Cisco37Controller(Controller):

    def __init__(self):
        super(Cisco37Controller, self).__init__()

    def checkPromptSuccess(self, prompt):
        return False if prompt.find('^') >= 0 else True

    def terLen(self):
        cmd = 'ter len 0'
        self.lastPrompt = self.channel.send_cmd(cmd)
        self.isLastCmdSuccess = self.checkPromptSuccess(self.lastPrompt)

    def config_syslog(self):
        config_txt = [
        "conf t",
        "logg trap warnings",
        "logging source-interface vlan666",
        "logging host 129.25.98.33",
        "exit",
        "wr"
        ]
        for line in config_txt:
            self.lastPrompt = self.channel.send_cmd(line)
            self.isLastCmdSuccess = self.checkPromptSuccess(self.lastPrompt)
            if self.isLastCmdSuccess == False:
                raise ConfigError('ConfigError, cmd is {cmd}, prompt is {prompt}'.format(cmd=line, prompt=self.lastPrompt))

    def ip_arp(self):
        cmd = 'sh ip arp'
        self.lastPrompt = self.channel.send_cmd(cmd)
        self.isLastCmdSuccess = self.checkPromptSuccess(self.lastPrompt)
        print(self.lastPrompt)

    #def login(self, xDevice):
    #    print('cisco37 login')
