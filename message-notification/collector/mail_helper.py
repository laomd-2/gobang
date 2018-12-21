# -*- coding: utf-8 -*-
import imaplib, email
import datetime
from email.header import decode_header
from email.utils import parseaddr


# *********接受邮件部分（IMAP）**********
# 处理接受邮件的类
class ReceiveMailDealer:

    # 构造函数(用户名，密码，imap服务器)
    def __init__(self, username, password, server):
        self.mail = imaplib.IMAP4_SSL(server)
        self.mail.login(username, password)
        self.select("INBOX")

    # 返回所有文件夹
    def show_folders(self):
        return self.mail.list()

    # 选择收件箱（如“INBOX”，如果不知道可以调用showFolders）
    def select(self, selector):
        return self.mail.select(selector)

    def add_flag(self, num, flag):
        self.mail.store(num, '+FLAGS', flag)

    def expunge(self):
        self.mail.expunge()

    # 返回所有未读的邮件列表（返回的是包含邮件序号的列表）
    def get_unread(self):
        untagged = self.mail.search(None, "Unseen")[1]
        return untagged[0].split()

    # 以RFC822协议格式返回邮件详情的email对象
    def get_email_format(self, num):
        data = self.mail.fetch(num, 'RFC822')
        if data[0] == 'OK':
            return email.message_from_string(data[1][0][1].decode('utf-8'))
        else:
            return "fetch error"

    # 返回发送者的信息——元组（邮件称呼，邮件地址）
    @staticmethod
    def get_sender_info(msg):
        name = parseaddr(msg["from"])[0]
        de_name = decode_header(name)[0]
        if de_name[1] is not None:
            name = de_name[0].decode(de_name[1])
        address = parseaddr(msg["from"])[1]
        return name, address

    # 返回接受者的信息——元组（邮件称呼，邮件地址）
    @staticmethod
    def get_receiver_info(msg):
        name = parseaddr(msg["to"])[0]
        de_name = decode_header(name)[0]
        if de_name[1] is not None:
            name = de_name[0].decode(de_name[1])
        address = parseaddr(msg["to"])[1]
        return name, address

    # 返回邮件的主题（参数msg是email对象，可调用getEmailFormat获得）
    @staticmethod
    def get_subject_content(msg):
        de_content = decode_header(msg['subject'])[0]
        if de_content[1] is not None:
            return de_content[0].decode(de_content[1])
        return de_content[0]

    @staticmethod
    def get_date_info(msg):
        date = email.header.decode_header(msg['date'])
        utcstr = date[0][0].split(' ')
        while ':' not in utcstr[-1]:
            utcstr.pop()
        utcstr = ' '.join(utcstr)
        return datetime.datetime.strptime(utcstr, '%a, %d %b %Y %H:%M:%S')

    '''返回邮件的解析后信息部分
    返回列表包含（主题，纯文本正文部分，html的正文部分，发件人元组，收件人元组，附件列表）
    '''

    def get_mail_info(self, num):
        msg = self.get_email_format(num)
        attachments = []
        body = ''
        html = ''
        for part in msg.walk():
            if part.get_content_type() == "text/plain":
                body += part.get_payload()
            elif part.get_content_type() == "text/html":
                html += part.get_payload()
        return {
            'id': msg.get('Message-ID'),
            'subject': self.get_subject_content(msg),
            'body': body,
            'html': html,
            'from': self.get_sender_info(msg),
            'to': self.get_receiver_info(msg),
            'date': self.get_date_info(msg),
            'attachments': attachments
        }
