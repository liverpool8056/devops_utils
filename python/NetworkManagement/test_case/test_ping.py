import sys
sys.path.append('/opt/tools/python/')
from NetworkManagement.ping import PingTool

if __name__ == '__main__':
    netSeg = '10.20.97.0/24'
    pt = PingTool(netSeg)
    pt.probe().filter().report()
