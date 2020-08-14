import json

class BaseModel:
    def items(self):
        ret = dict()
        attr_items = self.__dict__.items()
        for attr, value in attr_items:
            if attr.startswith('_'):
                continue
            value = value if type(value) == 'str' else str(value)
            ret.update({attr:value})
        return ret
