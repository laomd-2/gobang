import itchat
import time
from itchat.content import *

__msg_queue = None
__all__ = ['main_loop', 'log_in']


@itchat.msg_register(TEXT)
def friend_msg_event(msg):
    content = msg['Content']
    friend = '微信“%s”' % msg['User']['NickName']
    print('[%s] [INFO] 来自 %s 的消息："%s"' % (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                                          friend, content))
    __msg_queue.put((friend, content))


@itchat.msg_register(TEXT, isGroupChat=True)
def group_msg_event(msg):
    content = msg['Content']
    room = '微信群“%s”' % msg['User']['NickName']
    from_who = msg['ActualNickName']
    from_user = room + '[成员“%s”]' % (from_who if from_who else '我')
    print('[%s] [INFO] 来自 %s 的消息："%s"' % (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                                          from_user, content))
    if from_who:
        if '@ME' in content or '@所有人' in content:
            content = content.strip("[@ME]所有人 ")
            if content:
                __msg_queue.put((room + from_user, content))



def main_loop():
    itchat.run()


def log_in(msg_queue):
    global __msg_queue
    itchat.auto_login(hotReload=True)
    __msg_queue = msg_queue
