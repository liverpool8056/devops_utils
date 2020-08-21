class ChannlInitError(Exception):
    pass

class Channel:

    def __init__(self, xDevice):
        self.device = xDevice

        host_ip = self.device.managementIP
        tc = TelnetClient(self.device.managementIP)
        tc.comm_connect()
        if tc.err_type:
            raise ChannelInitError('Cannot connect to {hostname}({ip}), err_msg: {err_msg}'.format(hostname=self.device.name, ip=self.device.managementIP, err_msg=tc.err_type))
        self.channel = tc

    def raw_config(self, config_txt):
        self.tc. 
