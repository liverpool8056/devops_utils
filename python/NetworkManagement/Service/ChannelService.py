class Channel:

    def __init__(self, xDevice):
        self.device = xDevice

        host_ip = self.device.managementIP
        tc = TelnetClient(self.device.managementIP)
        tc.comm_connect()
        if tc.err_type:
            
