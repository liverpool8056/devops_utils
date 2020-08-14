from NetworkManagement.snmp import NDCollector

class IOS:
    oids = [
        'iso.0.8802.1.1.2.1.5.4795.1.2.4.0',
        'iso.0.8802.1.1.2.1.5.4795.1.2.7.0',
        'iso.0.8802.1.1.2.1.5.4795.1.2.6.0',
        'iso.0.8802.1.1.2.1.5.4795.1.2.2.0'
    ]
    def __init__(self):
        pass
    
    def snmp(self, ip):
        snmp_output = dict(ip=str(ip), isSnmpReachable=True) 
        for oid in IOS.oids:
            oid_v = NDCollector.snmp(ip, oid)
            if oid_v is None:
                snmp_output.update(dict(isSnmpReachable=False) )
                break
            snmp_output.update({oid:oid_v})
        return snmp_output

class IOS_XE(IOS):
    pass
            
class NX_OS:
    oids = []

    def __init__(self):
        pass
    
    def snmp(self, ip):
        snmp_output = dict(ip=str(ip), isSnmpReachable=True) 
        for oid in NX_OS.oids:
            oid_v = NDCollector.snmp(ip, oid)
            if oid_v is None:
                snmp_output.update(dict(isSnmpReachable=False) )
                break
            snmp_output.update({oid:oid_v})
        return snmp_output

class Huawei:
    oids = []

    def __init__(self):
        pass
    
    def snmp(self, ip):
        snmp_output = dict(ip=str(ip), isSnmpReachable=True) 
        for oid in Huawei.oids:
            oid_v = NDCollector.snmp(ip, oid)
            if oid_v is None:
                snmp_output.update(dict(isSnmpReachable=False) )
                break
            snmp_output.update({oid:oid_v})
        return snmp_output
