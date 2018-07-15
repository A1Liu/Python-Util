# -*- coding: utf-8 -*-

def contents(module,include_hidden = False):
    print('from {} import '.format(module),end = '')
    for name in dir(module):
        if not name.startswith('_') or include_hidden:
            print(name,end = ',')