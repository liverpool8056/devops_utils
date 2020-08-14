import telnetlib
import socket

#PROMPT_USERNAME = ['sername: ', 'ogin: ']
#PROMPT_USERNAME = ['aa: '.encode(), 'bb: '.encode()]
PROMPT_USERNAME = ['sername: '.encode(), 'ogin: '.encode(), 'sername:'.encode()]
#PROMPT_PASSWORD = ['assword: ']
PROMPT_PASSWORD = ['assword: '.encode(), 'assword:'.encode()]
#PROMPT_RAW = ['#', '>', ']', '$']
PROMPT_RAW = ['#'.encode(), '>'.encode(), ']'.encode(), '\$'.encode()]
PROMPT_PREFIX_SUFFIX = '[]#<>$'
USERNAME_SH = 'xiangwenchao'
PASSWORD_SH = 'Check1234'
USERNAME_FZ = 'xiangwc'
PASSWORD_FZ = 'QWERasdf1234=-'


class TelnetClient:
    
    def __init__(self, host, port=23, timeout=5):
        self.host_info = dict(host=host, port=port)
        self.timeout = timeout
        self.err_type = None
        self.hostname = ''
        self.err_prompt = ''
    
    def comm_connect(self):
        try:
            self.tn = telnetlib.Telnet(self.host_info['host'], port=23, timeout=3)
            #self.tn = telnetlib.Telnet(Host, port=23, timeout=3)
        except (socket.timeout, OSError, NameError) as e:
            self.tn = None
            self.err_type = e
            return

        self.tn.set_debuglevel(0)
        out = self.tn.expect(PROMPT_USERNAME, timeout=self.timeout)
        if out[0] < 0:
            self.err_type = 'Unrecognized prompt'
            self.err_prompt = out[2]
            self.close()
            return
        self.tn.write((USERNAME_SH + '\n').encode())
        out = self.tn.expect(PROMPT_PASSWORD, timeout=self.timeout)
        if out[0] < 0:
            self.err_type = 'Unrecognized prompt'
            self.err_prompt = out[2]
            self.close()
            return
        self.tn.write((PASSWORD_SH + '\n').encode())
        out = self.tn.expect(PROMPT_RAW, timeout=self.timeout)	
        if out[0] < 0:
            self.err_type = 'Wrong username or password'
            self.err_prompt = out[2]
            self.close()
            return
        #print(out[2].decode().strip())
        self.get_raw_name(out[2].decode().split('\r\n')[-1].strip())

    def get_raw_name(self, prompt):
        self.hostname= prompt.strip(PROMPT_PREFIX_SUFFIX)

    def isConnected(self):
        return True if self.tn else False

    def close(self):
        self.tn.close()
        self.tn = None

if __name__ == '__main__':
    #Host = '1.20.100.80'
    Host = '10.20.100.92'
    tc = TelnetClient(Host)
    tc.comm_connect()
    if tc.isConnected():
        print('Success to connect to {hostname}({host})'.format(hostname=tc.hostname, host=Host))
        tc.close()
    else: 
        print('Fail to connect to {hostname}({host}), err_type is {err_type}, err_prompt is {err_prompt}'.format(hostname=tc.hostname, host=Host, err_type=tc.err_type, err_prompt=tc.err_prompt))
