from datetime import datetime


def Log(msg):
    with open('./log.txt', 'a+') as file:
        file.write('%s: %s\n' %(datetime.now(), msg))


if __name__ == '__main__':
    print('这是日志模块，将调试的信息记录到log.txt文件中')