from NetworkManagement.utils.redis_conn import redis_conn
from NetworkManagement.snmp import NDCollector

class xDevice:
    sysOid = 'SNMPv2-MIB::sysObjectID.0'

    def __init__(self, managementIP, name='', secondaryIPs=[], zone='', location='', tags=[], description='', serialNum='', model='', version='', manufacturer='', comment='', credential=None, status='', ssh_enabled=False, telnet_enabled=False, isICMPReachable=False, isSNMPReachable=False, **kwargs):
        self.name = name 
        self.managementIP = managementIP
        self.secondaryIPs = secondaryIPs
        self.zone = zone
        self.location = location
        self.tags = tags
        self.description = description
        self.serialNum= serialNum
        self.model= model
        self.version = version
        self.manufacturer = manufacturer
        self.comment = comment
        self.credential =credential
        self.status = status
        self.ssh_enabled = ssh_enabled
        self.telnet_enabled = telnet_enabled
        self.isICMPReachable = isICMPReachable
        self.isSNMPReachable = isSNMPReachable

        self._redis_conn = redis_conn
    
    def render(self):
        self._sysOid = self.__get_sysOid()
        if self._sysOid:
            self.isSNMPReachable = True
            oids = self.get_oidlist(self._sysOid)
            for key in oids:
                if key not in ['version', 'name', 'manufacturer', 'model']:
                    continue
                value = NDCollector.snmp(self.managementIP, oids[key])
                #if value is None: 
                    #print('{ip}-{sysoid}-{key}:{oid}'.format(ip=self.managementIP, sysoid=self._sysOid, key=key, oid=oids[key]))
                 
                #if 'Unknown Object Identifier' in value:
                    #print('{ip}-{key}:{oid}'.format(ip=self.managementIP, key=key, oid=oids[key]))
              
                if key == 'version':
                    self.version = value
                elif key == 'name':
                    self.name = value
                elif key == 'model':
                    self.model = value
                elif key == 'manufacturer':
                    self.manufacturer = value

    def to_redis_value(self):
        ret = dict()
        attr_items = self.__dict__.items()
        for attr, value in attr_items:
            if attr.startswith('_'):
                continue
            value = value if type(value) == 'str' else str(value)
            ret.update({attr:value})
        return ret

    def get_oidlist(self, sysOid):
        key_patten = 'sysOid:{sysOid}'
        key = key_patten.format(sysOid=self._sysOid)
        return self._redis_conn.hgetall(key)

    def __get_sysOid(self):
        sysOid = NDCollector.get_sysOid(self.managementIP)
        return sysOid

    def __str__(self):
        return str(self.to_redis_value())

