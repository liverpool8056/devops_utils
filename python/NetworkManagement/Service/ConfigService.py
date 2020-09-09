from NetworkManagement.utils.redis_conn import redis_conn
from NetworkManagement.Models.deviceConfig import DeviceConfig
import datetime

class ConfigService:
    def __init__(self):
        self.redis_conn = redis_conn

    def save(self, config):
        ts = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        config.set_timestamp(ts)
        key_pattern = 'config:{host}:{day}'
        key = key_pattern.format(host=config.owner, day=ts.split(' ')[0])
        self.redis_conn.hmset(key, config.items())

    def get(self, obj):
        # type obj is NetworkDevice
        key_pattern = 'config:{host}'
        host = obj.managementIP
        key = key_pattern.format(host=host)
        config_dict = self.redis_conn.hgetall(key)
        return DeviceConfig(**config_dict)
