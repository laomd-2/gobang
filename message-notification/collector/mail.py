import calendar, time
from .mail_helper import ReceiveMailDealer
from datetime import datetime
from qqbot.utf8logger import INFO, ERROR


__msg_queue = None
server: ReceiveMailDealer = None


def log_in(msg_queue, **kwargs):
    global __msg_queue, server
    __msg_queue = msg_queue
    user = kwargs['user']
    server_addr = kwargs.get('server', None) or 'pop.' + user.split('@')[1]
    password = kwargs.get('password', None) or input('password: ')
    server = ReceiveMailDealer(user, password, server_addr)


def to_datetime(str_datetime):
    mon = dict((v, k) for k, v in enumerate(calendar.month_abbr))
    str_datetime = str_datetime.split(' ')[1:-2]
    str_datetime[1] = str(mon[str_datetime[1]])
    tmp = list(map(int, str_datetime.pop().split(':')))
    str_datetime = list(map(int, reversed(str_datetime)))
    return datetime(*str_datetime, *tmp)


def main_loop():
    read = set()
    while True:
        try:
            # 遍历未读邮件
            for num in reversed(server.get_unread()):
                if num != '':
                    mail_info = server.get_mail_info(num)
                    mail_id = mail_info['id']
                    if mail_id in read:
                        break
                    content = mail_info['subject'].replace('\n', '')
                    app = "邮箱(" + mail_info['to'][1] + ')'
                    who = mail_info['from'][0]
                    INFO('来自%s%s的邮件：%s' % (app, who, content))
                    __msg_queue.put((app, who, content))
                    read.add(mail_id)
            time.sleep(3)
        except Exception as e:
            raise e
            ERROR(str(type(e)) + str(e))
