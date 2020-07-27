import sys
sys.path.append('/opt/tools/python')
from NetworkManagement.ping import PingTool
from NetworkManagement.segment_collector import NetSegmentProxy
from NetworkManagement.snmp import NDCollector
import json

if __name__ == '__main__':
    netProxy = NetSegmentProxy()
    segments = netProxy.get_segments()
    snmp_result = []
    for segment in segments:
        pt = PingTool(segment.decode())
        #pt.probe().filter().report()
        reachableIPs = pt.reachableIPs()
        for ip in reachableIPs:
            snmp_result_per_device = NDCollector.run(ip)
            if not snmp_result_per_device.get('isSnmpReachable'):
                break
            snmp_result.append(snmp_result_per_device)
    with open('./snmp_result.txt', 'w') as f:
        f.write(json.dumps(snmp_result))
    print('Finish')
