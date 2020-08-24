from NetworkManagement.utils.redis_conn import redis_conn
import json

def pushConfig2Redis(os_type, feature, contents):
    key = f'networkConfig:{os_type}:{feature}'

    lines = contents.split('\r\n') if type(contents) == str else contents
    
    value = dict(
        lines=json.dumps(lines)
    )

    redis_conn.hmset(key, value)

if __name__ == '__main__':
    os_type = 'IOS'
    feature = 'syslog'
    contents = [ 
        "conf t",
        "logg trap warnings",
        "logging source-interface vlan666",
        "logging host 129.25.98.33",
        "exit",
        "wr"
    ]
    
    pushConfig2Redis(os_type, feature, contents)
    
    key = 'networkConfig:IOS:syslog'
    ret = redis_conn.hgetall(key)
    print(json.loads(ret.get('lines')))
