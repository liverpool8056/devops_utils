import json
from NetworkManagement.utils.redis_conn import redis_conn
from NetworkManagement.Models.segment import Segment

class SegmentService:

    def __init__(self):
        self.redis_conn = redis_conn

    def save(self, segment):
        key_pattern = 'segment:{segment}/{mask}'
        key = key_pattern.format(segment=segment.segment, mask=segment.mask)
        self.redis_conn.hmset(key, segment.items())

    def load_from_file(self, fpath):
        with open(fpath) as f:
            segment_list = json.loads(f.read())
        return segment_list

    def getAllSegment(self):
        seg_list = []
        key_pattern = 'segment:*'
        seg_keys = self.redis_conn.keys(key_pattern)
        for key in seg_keys:
            seg = Segment(**self.redis_conn.hgetall(key))
            seg_list.append(seg)
        return seg_list
    
    def getSegmentByZone(self, zone):
        seg_list = self.getAllSegment()
        seg_list = [ seg for seg in seg_list if seg.zone==zone ]
        return seg_list
