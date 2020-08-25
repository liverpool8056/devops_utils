from NetworkManagement.telnet_client import TelnetClient

if __name__=='__main__':
    host = '10.20.100.217' #IOS
    host = '10.20.100.220' #N3K
    tc = TelnetClient(host)
    tc.comm_connect()
    
    hostname = tc.get_raw_name()
    print(hostname, tc.hostname)
    
    config_txt = 'wr'
    res = tc.send_cmd(config_txt)
    print(res)

    tc.close()
