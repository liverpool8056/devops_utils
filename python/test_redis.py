from NetworkManagement.utils.redis_conn import redis_conn
import json

class Test:
    def __init__(self):
        self.a = 1
    def b(self):
        print('This is a method')
    def get_attr(self):
        att_list = self.__dict__
        print(att_list)
    def get_func(self):
        func_list = self.__func__
        print(func_list)
    def get_module(self):
        module_list = self.__module__
        print(module_list)

if __name__ == '__main__':
    #value = dict(bool_value = str([]))
    #key = 'test'
    #redis_conn.hmset('test', value)
    t = Test()
    t.b()
    t.get_attr()
    t.__getattribute__
    #t.get_module()
    #t.get_func()
    #print(dir(t))
