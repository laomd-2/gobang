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
    auto_dl = kwargs.get('auto_download', False)
    server = ReceiveMailDealer(user, password, server_addr, auto_dl)


def to_datetime(str_datetime):
    mon = dict((v, k) for k, v in enumerate(calendar.month_abbr))
    str_datetime = str_datetime.split(' ')[1:-2]
    str_datetime[1] = str(mon[str_datetime[1]])
    tmp = list(map(int, str_datetime.pop().split(':')))
    str_datetime = list(map(int, reversed(str_datetime)))
    return datetime(*str_datetime, *tmp)


def main_loop():
    abstract = ['subject']
    read = set()
    while True:
        try:
            # 遍历未读邮件
            for num in reversed(server.get_unread()[1][0].split()):
                if num != '':
                    mail_info = server.get_mail_info(num)
                    id = mail_info['id']
                    if id in read:
                        break
                    content = '\r\n'.join([mail_info[k].replace('\n', '') for k in abstract])
                    if server.auto_download:
                        # 遍历附件列表
                        for attachment in mail_info['attachments']:
                            with open(attachment['name'], 'wb') as fileob:
                                fileob.write(attachment['data'])
                    app = "邮箱(" + mail_info['to'][1] + ')'
                    who = mail_info['from'][0]
                    INFO('来自%s%s的邮件：%s' % (app, who, content))
                    __msg_queue.put((app, who, content))
                    read.add(id)
            time.sleep(3)
        except Exception as e:
            ERROR(str(type(e)) + str(e))
