import redis

REDIS_HOST = '10.20.97.101'
REDIS_PORT = 6379

class NetSegmentProxy:
    
    def __init__(self):
        self.redis = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=0)

    def get_segments(self):
        """
        rtype: set
        """
        return self.redis.smembers('netSegment:deviceManage')


if __name__ == '__main__':
    netProxy = NetSegmentProxy()
    segments = netProxy.get_segments()

    print('finish')
