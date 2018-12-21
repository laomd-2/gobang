import itchat, time
from itchat.content import *
from qqbot.utf8logger import INFO, ERROR

__msg_queue = None
__all__ = ['main_loop', 'log_in']


def is_me(msg):
    me = itchat.originInstance.loginInfo['User']
    return msg['FromUserName'] == me['UserName']


@itchat.msg_register(TEXT)
def friend_msg_event(msg):
    content = msg['Content']
    friend = msg['User']
    friend_name = friend['UserName']
    try:
        friend_name = friend['NickName']
        friend_name = friend['RemarkName']
    except KeyError:
        pass
    friend_name = '“%s”' % friend_name
    INFO('来自 %s 的消息："%s"' % (friend_name, content))
    if is_me(msg):
        return
    __msg_queue.put(("微信", friend_name, content))


@itchat.msg_register(TEXT, isGroupChat=True)
def group_msg_event(msg):
    content = msg['Content']
    room = '微信-群“%s”' % msg['User']['NickName']
    from_who = msg['ActualNickName']
    from_user = room + '[成员“%s”]' % (from_who if from_who else '我')
    INFO('来自 %s 的消息："%s"' % (from_user, content))
    if is_me(msg):
        return
    if msg.IsAt:
        content = content.strip("[@ME]所有人 ")
        if content:
            __msg_queue.put((room + from_user, content))


def main_loop():
    while True:
        try:
            itchat.run()
        except Exception as e:
            ERROR(e)
            time.sleep(3)


def log_in(msg_queue):
    global __msg_queue
    itchat.auto_login(hotReload=True)
    __msg_queue = msg_queue
