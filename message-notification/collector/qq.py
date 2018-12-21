from qqbot import QQBotSlot
from qqbot import _bot as bot
from qqbot.utf8logger import ERROR
import time

__msg_queue = None


@QQBotSlot
def onQQMessage(bot, contact, member, content):
    if bot.isMe(contact, member):
        return
    if contact.ctype != 'buddy' and ('@ME' in content or '@全体成员' in content):
        content = content.strip("[@ME]全体成员 ")
        if content:
            __msg_queue.put(("QQ", "群" + contact.name + '/' + member.name, content))


def log_in(user_qq, msg_queue):
    global __msg_queue
    __msg_queue = msg_queue
    bot.Login(['-q', user_qq])


def main_loop():
    while True:
        try:
            bot.Run()
        except Exception as e:
            ERROR(e)
            time.sleep(3)
