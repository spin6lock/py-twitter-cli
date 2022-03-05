#encoding:utf8
#credited for: https://stackoverflow.com/questions/1305532/convert-nested-python-dict-to-object @JayD3e
import pprint
pformat = pprint.pformat

class DictProxy(object):
    def __init__(self, obj):
        self.obj = obj

    def __getitem__(self, key):
        return wrap(self.obj[key])

    def __getattr__(self, key):
        try:
            return wrap(getattr(self.obj, key))
        except AttributeError:
            try:
                return self[key]
            except KeyError:
                #raise AttributeError(key)
                return None

    def __repr__(self):
        return pformat(self.obj)

    # you probably also want to proxy important list properties along like
    # items(), iteritems() and __len__

class ListProxy(object):
    def __init__(self, obj):
        self.obj = obj

    def __getitem__(self, key):
        return wrap(self.obj[key])

    def __len__(self):
        return len(self.obj)
    # you probably also want to proxy important list properties along like
    # __iter__ and __len__

def wrap(value):
    if isinstance(value, dict):
        return DictProxy(value)
    if isinstance(value, (tuple, list)):
        return ListProxy(value)
    return value
