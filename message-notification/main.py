import threading
import sys
from queue import Queue
from notifier.MyToastNotifier import MyToastNotifier
from collector import wechat, qq

msg_queue = Queue(100)


def consumer():
    ignore = 1
    while True:
        title, content = msg_queue.get()
        if ignore > 0:
            ignore -= 1
            continue
        toaster.show_toast(title, content, duration=0.1, threaded=True)


if __name__ == '__main__':
    wechat.log_in(msg_queue)
    qq.log_in("965524991", sys.argv[1:], msg_queue)
    toaster = MyToastNotifier()
    threading.Thread(target=consumer).start()
    threading.Thread(target=wechat.main_loop).start()
    qq.main_loop()