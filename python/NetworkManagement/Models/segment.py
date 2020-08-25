from NetworkManagement.Models.baseModel import BaseModel
from NetworkManagement.Models.xIP import xIP
from IPy import IP

class Segment(BaseModel):
    
    gw_index = 0
    start = gw_index + 1
    end = 255

    def __init__(self, segment='', mask=24, zone='', role='', location='', tags=[]):
        self.segment=segment
        self.mask = mask
        self.zone = zone
        self.role = role
        self.location = location
        self.tags = tags

    def get_hosts(self):
        ips = []
        segment_mask = '{segment}/{mask}'.format(segment=self.segment, mask=self.mask)
        seg = IP(segment_mask)
        for ip in seg[Segment.start:Segment.end]:
            ip = str(ip)
            zone = self.zone
            xip = xIP(ip, zone=zone)
            ips.append(xip)
        return ips
