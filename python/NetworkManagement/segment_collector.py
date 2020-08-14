#import redis

#REDIS_HOST = '10.20.97.101'
#REDIS_PORT = 6379
from NetworkManagement.utils.redis_conn import redis_conn

#class Segment:

    #def __init__(self, segment, mask, zone, location):
        #self.segment = segment

class NetSegmentProxy:
    key_pattern = 'segment:{segment}'
    
    def __init__(self):
        #self.redis = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=0, decode_responses=True)
        self.redis = redis_conn

    def get_segments(self):
        """
        rtype: set
        """
        return list(self.redis.smembers('netSegment:deviceManage'))

    def get_segment(self, segment):
        key = NetSegmentProxy.key_pattern.format(segment=segment)
        return self.redis.hgetall(key)


if __name__ == '__main__':
    netProxy = NetSegmentProxy()
    segments = netProxy.get_segments()
    print(netProxy.get_segment(segments[0]))

    print('finish')
