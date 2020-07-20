import telnetlib
import socket

PROMPT_USERNAME = 'sername: '
PROMPT_PASSWORD = 'assword: '

USERNAME_SH = 'xiangwenchao'
PASSWORD_SH = 'Check1234'
USERNAME_FZ = 'xiangwc'
PASSWORD_FZ = 'QWERasdf1234=-'


class TelnetClient:
    
    def __init__(self, host, port=23, timeout=3):
        self.host_info = dict(host=host, port=port)
        self.timeout = timeout
    
    def connect(self):
        try:
            self.tn = telnetlib.Telnet(Host, port=23, timeout=3)
        except (socket.timeout, OSError, NameError):
            self.tn = None
            return

        tn.set_debuglevel(0)
        tn.read_until(PROMPT_USERNAME.encode())
        tn.write((USERNAME_SH + '\n').encode())
        tn.read_until(PROMPT_PASSWORD.encode())
        tn.write((PASSWORD_SH + '\n').encode())
        tmp_str = tn.read_until('#'.encode())	
        print(tmp_str.decode().strip())

    def isConnected(self):
        return True if self.tn else False

    def close(self):
        self.tn.close()

if __name__ == '__main__':
    Host = '1.20.100.80'
    #Host = '10.20.100.80'
    tc = TelnetClient(Host)
    tc.connect()
    if tc.isConnected():
        print('Success to connect to <{host}>'.format(host=Host))
    else: 
        print('Fail to connect to <{host}>'.format(host=Host))
