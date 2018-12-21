import threading
import sys
import argparse
from queue import Queue
from notifier.MyToastNotifier import MyToastNotifier, ToastNotifier
from collector import wechat, qq, mail

msg_queue = Queue(100)


def consumer():
    ignore = 0
    while True:
        title, who, content = msg_queue.get()
        if ignore > 0:
            ignore -= 1
            continue
        toaster.show_toast(title + '  ' + who, content, duration=2)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(allow_abbrev=True)
    parser.add_argument('-w', '--wechat', action="store_true", default=False)
    parser.add_argument('-q', '--qq', action="store")
    parser.add_argument('-u', '--user', action="store")
    parser.add_argument('-p', '--password', action="store")
    parser.add_argument('-s', '--server', action="store", default='pop.exmail.qq.com')
    params = parser.parse_args(sys.argv[1:])

    toaster = ToastNotifier()
    workers = [consumer]

    if params.wechat:
        wechat.log_in(msg_queue)
        workers.append(wechat.main_loop)
    if params.user:
        mail.log_in(msg_queue, user=params.user, password=params.password, server=params.server)
        workers.append(mail.main_loop)
    if params.qq:
        qq.log_in(params.qq, msg_queue)
        workers.append(qq.main_loop)
    if len(workers) > 1:
        for w in workers[:-1]:
            threading.Thread(target=w).start()
        workers[-1]()
