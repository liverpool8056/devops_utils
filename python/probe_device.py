from NetworkManagement.Service.SegmentService import SegmentService
from NetworkManagement.Service.DeviceService import NetworkDeviceService
from NetworkManagement.Models.networkDevice import xDevice
from NetworkManagement.ping import PingTool

if __name__ == '__main__':
    segSvc = SegmentService()
    netDevSvc = NetworkDeviceService()
    seg_list = segSvc.getSegmentByZone('M')


    location = 'sh'
    
    for seg in seg_list:
       print(seg.items())
       if seg.location != location:
           continue
       pt = PingTool(seg.segment+'/'+str(seg.mask))
       pt.probe().filter()
       reachable_ip_list = [ r[0] for r in pt.result ]
       for ip in reachable_ip_list:
           print(ip)
           d = xDevice(ip, zone=seg.role, location=seg.location)
           d.render()
           netDevSvc.save(d)
