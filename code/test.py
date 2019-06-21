import sys


class Test:
    def __init__(self):
        self.m_debug = False

    def logOn(self):
        self.m_debug = True

    def logOff(self):
        self.m_debug = False

    def log(self, msg):
        if self.m_debug:
            print('in file [%s] function (%s) line {%s}:' % (__file__.split('/')[-1], sys._getframe().f_code.co_name, sys._getframe().f_lineno))
            print(msg)

if __name__ == '__main__':
    print("这是为了测试而产生的模块，所有的类都需要继承Test类以便调试当调用logOn()的时候会调试")
    print("接下来是本模块的测试")
    t = Test()
    t.logOn()
    t.log('this is a message')