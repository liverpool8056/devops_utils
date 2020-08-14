from NetworkManagement.Models.baseModel import BaseModel

class xIP(BaseModel):

    def __init__(self, ip, zone='', status='', isReachable=False):
        self.ip = ip 
        self.zone = zone
        self.status = status
        self.isReachable = isReachable
