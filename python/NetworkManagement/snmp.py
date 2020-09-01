import pprint
import os
import json

class NDCollector:
    oids = [
        'SNMPv2-MIB::sysObjectID.0',
        'SNMPv2-MIB::sysName.0',
        'SNMPv2-MIB::sysDescr.0',
        #'iso.0.8802.1.1.2.1.5.4795.1.2.4.0',
        #'iso.0.8802.1.1.2.1.5.4795.1.2.7.0',
        #'iso.0.8802.1.1.2.1.5.4795.1.2.6.0',
        #'iso.0.8802.1.1.2.1.5.4795.1.2.2.0'
    ]
    snmp_cmd = "snmpwalk -v 2c -Ovq -t 1 -r 1 -c xyzqnetmanager {ip} {oid}"

    @staticmethod
    def run(ip):
        snmp_output = dict(ip=str(ip), isSnmpReachable=True) 
        for oid in NDCollector.oids:
            oid_v = NDCollector.snmp(ip, oid)
            if oid_v is None:
                snmp_output.update(dict(isSnmpReachable=False) )
                break
            snmp_output.update({oid:oid_v})
        return snmp_output

    @staticmethod
    def get_sysOid(ip):
        return NDCollector.snmp(ip, NDCollector.oids[0])
        
    def __init__(self):
        pass
    
    @staticmethod
    def snmp(ip, oid):
        f = os.popen(NDCollector.snmp_cmd.format(ip=ip, oid=oid))
        oid_v = f.read().strip().strip('"')
        return None if "Timeout" in oid_v or len(oid_v) == 0 or oid_v.lower().find("no such")>=0 else oid_v

if __name__ == "__main__":
    oids = [
        'iso.0.8802.1.1.2.1.5.4795.1.2.4.0',
        'iso.0.8802.1.1.2.1.5.4795.1.2.7.0',
        'iso.0.8802.1.1.2.1.5.4795.1.2.6.0',
        'iso.0.8802.1.1.2.1.5.4795.1.2.2.0'
    ]
    #ip = '10.20.100.226'
    #Bangong-5F-3850-1, WS-C3850-24T
    ip = '10.20.100.50'
    result = NDCollector.run(ip)
    print(result)
    for oid in oids:
        result = NDCollector.snmp(ip, oid)
        print(oid,result)
