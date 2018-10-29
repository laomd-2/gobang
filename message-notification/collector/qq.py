from qqbot import QQBotSlot
from qqbot import _bot as bot

__msg_queue = None


@QQBotSlot
def onQQMessage(bot, contact, member, content):
    if contact.ctype == 'buddy' or '@ME' in content or '@全体成员' in content:
        content = content.strip("[@ME]全体成员 ")
        if content:
            __msg_queue.put((contact.name + '/' + member.name, content))


def log_in(user_qq, argv, msg_queue):
    global __msg_queue
    __msg_queue = msg_queue
    if user_qq:
        argv += ['-q', user_qq]
    bot.Login(argv)


def main_loop():
    bot.Run()
