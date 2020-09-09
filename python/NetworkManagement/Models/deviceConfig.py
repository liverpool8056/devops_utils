from NetworkManagement.utils.redis_conn import redis_conn
from NetworkManagement.Models.baseModel import BaseModel

class DeviceConfig(BaseModel):

    def __init__(self, owner='', value=''):
        self.owner = owner
        self.value = value

    def set_timestamp(self, ts_str):
        self.timestamp = ts_str
