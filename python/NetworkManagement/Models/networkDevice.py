from NetworkManagement.utils.redis_conn import redis_conn
from NetworkManagement.snmp import NDCollector
from NetworkManagement.Models.baseModel import BaseModel

class BoolChecker:

    def __init__(self, val=False, name='var'):
        self.name = name
        self.val = val

    def __get__(self, instance, owner):
        if instance is None:
            return self
        else:
            return instance.__dict__[self.name]

    def __set__(self, instance, val):
        if isinstance(val, bool):
            instance.__dict__[self.name] = val
        elif isinstance(val, str):
            if val == 'True':
                instance.__dict__[self.name] = True
            elif val == 'False':
                instance.__dict__[self.name] = False
            else:
                raise AttributeError('Attribute Error, expect type of {attr_name} is \'bool\' or \'str\', but {val_type} received'.format(attr_name=self.name, val_type=type(val)))
        else:
            raise AttributeError('Attribute Error, expected type of {attr_name} is \'bool\' or \'str\', but {val_type} received'.format(attr_name=self.name, val_type=type(val)))
            

class xDevice(BaseModel):
    sysOid = 'SNMPv2-MIB::sysObjectID.0'
    ssh_enabled = BoolChecker(False, 'ssh_enabled')
    telnet_enabled = BoolChecker(False, 'telnet_enabled')
    isICMPReachable = BoolChecker(False, 'isICMPReachable')
    isSNMPReachable = BoolChecker(False, 'isSNMPReachable')

    def __init__(self, managementIP, sysOid='', name='', deviceType='', secondaryIPs=[], zone='', location='', tags=[], description='', serialNum='', model='', version='', manufacturer='', comment='', credential=None, status='', ssh_enabled=False, telnet_enabled=False, isICMPReachable=False, isSNMPReachable=False, **kwargs):
        self.managementIP = managementIP
        self.sysOid = sysOid
        self.name = name 
        self.deviceType = deviceType
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

    def __snmp_oids(self, oids):
        oids = oids.split(',')
        for oid in oids:
            value = NDCollector.snmp(self.managementIP, oid.strip())
            if value:
                return value

    def render(self):
        self.sysOid = self.__get_sysOid()
        if self.sysOid:
            self.isSNMPReachable = True
            oid_dict = self.get_oidlist(self.sysOid)
            for key in oid_dict:
                if key in ['version', 'name', 'manufacturer', 'model']:
                   value = self.__snmp_oids(oid_dict[key])
                elif key in ['deviceType']:
                    #print('deviceType: {type}'.format(type=oid_dict[key]))
                    self.__dict__[key] = oid_dict[key]
              
                if key == 'version':
                    self.version = value
                elif key == 'name':
                    self.name = value
                elif key == 'model':
                    self.model = value
                elif key == 'manufacturer':
                    value = NDCollector.snmp(self.managementIP, 'SNMPv2-MIB::sysDescr.0') if value is None else value
                    value = value.split(',')[0].strip() if value else value
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
        key = key_patten.format(sysOid=self.sysOid)
        return self._redis_conn.hgetall(key)

    def __get_sysOid(self):
        sysOid = NDCollector.get_sysOid(self.managementIP)
        return sysOid

    def __str__(self):
        return str(self.to_redis_value())

