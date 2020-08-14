from NetworkManagement.utils.redis_conn import redis_conn
import redis

pingSrc = '10.20.97.100'

class IPService:
    
    def __init__(self):
        self.redis_conn = redis_conn

    def getAllIP(self):
        ips = []
        keys = self.redis_conn.keys('ip:*')
        for key in keys:
            ip = xIP(**self.redis_conn.hgetall(key))
            ips.append(ips)
       return ips
    
    def getIPByZone(self, zone):
        ips = self.getAllIP()
        ips = [ip for ip in ips if ip.zone==zone]
        return ips

    def save(self, xIp):
        key_pattern = 'ip:{ip}'
        key = key_pattern.format(ip=xIp.ip)
        self.redis_conn.hmset(key, xIP.items())
