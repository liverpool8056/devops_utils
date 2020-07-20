import pprint
import os
import json
from new_ping import PingTool

if __name__ == "__main__":
    segments = [
     "10.26.3.0/24",
     "10.20.100.0/24",
     "10.20.102.0/24",
     "10.26.2.0/24",
     "10.20.101.0/24",
     "10.20.103.0/24",
     "10.29.100.0/24",
     "10.20.105.0/24",
    ]
    oids = [
        'SNMPv2-MIB::sysName.0',
        'SNMPv2-MIB::sysObjectID.0',
        'SNMPv2-MIB::sysDescr.0',
        'iso.0.8802.1.1.2.1.5.4795.1.2.4.0',
        'iso.0.8802.1.1.2.1.5.4795.1.2.7.0',
        'iso.0.8802.1.1.2.1.5.4795.1.2.6.0',
        'iso.0.8802.1.1.2.1.5.4795.1.2.2.0'
    ]

    result = []

    for segment in segments:
        pt = PingTool(segment)
        pt.probe().filter()
        snmp_cmd = "snmpwalk -v 2c -Ovq -t 1 -r 1 -c xyzqnetmanager {ip} {oid}"
        for ip, state in pt.result:
            snmp_output = dict(ip=str(ip)) 
            for oid in oids:
                f = os.popen(snmp_cmd.format(ip=ip, oid=oid))
                oid_v = f.read().strip()
                if "Timeout" in oid_v:
                    snmp_output.update(dict(isReachable=False) )
                    break
                snmp_output.update({oid:oid_v})
            if "isReachable" not in snmp_output:
                snmp_output.update({"isReachable":True})
            result.append(snmp_output)
    ret = json.dumps(result)
    print(ret)
