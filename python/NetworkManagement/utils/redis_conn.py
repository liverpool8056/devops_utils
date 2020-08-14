import redis

REDIS_HOST = '10.20.97.101'
REDIS_PORT = 6379

redis_conn = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=0, decode_responses=True)
