import pprint
import os
import json
from .ping import PingTool

class NDCollector:
    oids = [
        'SNMPv2-MIB::sysName.0',
        'SNMPv2-MIB::sysObjectID.0',
        'SNMPv2-MIB::sysDescr.0',
        'iso.0.8802.1.1.2.1.5.4795.1.2.4.0',
        'iso.0.8802.1.1.2.1.5.4795.1.2.7.0',
        'iso.0.8802.1.1.2.1.5.4795.1.2.6.0',
        'iso.0.8802.1.1.2.1.5.4795.1.2.2.0'
    ]
    snmp_cmd = "snmpwalk -v 2c -Ovq -t 1 -r 1 -c xyzqnetmanager {ip} {oid}"

    def __init__(self):
        pass

    @staticmethod
    def run(ip):
        snmp_output = dict(ip=str(ip), isSnmpReachable=True) 
        for oid in NDCollector.oids:
            f = os.popen(NDCollector.snmp_cmd.format(ip=ip, oid=oid))
            oid_v = f.read().strip().strip('"')
            if "Timeout" in oid_v or len(oid_v) == 0:
                snmp_output.update(dict(isSnmpReachable=False) )
                break
            snmp_output.update({oid:oid_v})
        return snmp_output

if __name__ == "__main__":
    ip = '172.100.2.11'
    result = NDCollector.run(ip)
