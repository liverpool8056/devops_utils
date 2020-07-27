import sys
sys.path.append('/opt/tools/python')
from NetworkManagement.snmp import NDCollector

if __name__ == '__main__':
    nd = NDCollector()
    print(nd.run('172.100.2.2'))
