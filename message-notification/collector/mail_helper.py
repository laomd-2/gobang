# -*- coding: utf-8 -*-
import imaplib, email
import sys, datetime
from email.header import decode_header
from email.utils import parseaddr


# *********接受邮件部分（IMAP）**********
# 处理接受邮件的类
class ReceiveMailDealer:

    # 构造函数(用户名，密码，imap服务器)
    def __init__(self, username, password, server, auto_download):
        self.mail = imaplib.IMAP4_SSL(server)
        self.mail.login(username, password)
        self.auto_download = auto_download
        self.select("INBOX")

    # 返回所有文件夹
    def show_folders(self):
        return self.mail.list()

    # 选择收件箱（如“INBOX”，如果不知道可以调用showFolders）
    def select(self, selector):
        return self.mail.select(selector)

    # 搜索邮件(参照RFC文档http://tools.ietf.org/html/rfc3501#page-49)
    def search(self, charset, *criteria):
        try:
            return self.mail.search(charset, *criteria)
        except Exception as e:
            print(e.with_traceback(tb=sys.exc_info()[2]))
            self.select("INBOX")
            return self.mail.search(charset, *criteria)

    # 返回所有未读的邮件列表（返回的是包含邮件序号的列表）
    def get_unread(self):
        return self.search(None, "Unseen")

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

    '''判断是否有附件，并解析（解析email对象的part）
    返回列表（内容类型，大小，文件名，数据流）
    '''

    @staticmethod
    def parse_attachment(message_part, save=False):
        content_disposition = message_part.get("Content-Disposition", None)
        if content_disposition:
            dispositions = content_disposition.strip().split(";")
            if content_disposition and dispositions[0].lower() == "attachment":
                file_data = message_part.get_payload(decode=True)
                attachment = {"content_type": message_part.get_content_type(), "size": len(file_data)}
                de_name = decode_header(message_part.get_filename())[0]
                name = de_name[0]
                if de_name[1] is not None:
                    name = de_name[0].decode(de_name[1])
                attachment["name"] = name
                attachment["data"] = file_data
                # 保存附件
                if save:
                    fileobject = open(name, "wb")
                    fileobject.write(file_data)
                    fileobject.close()
                return attachment
        return None

    '''返回邮件的解析后信息部分
    返回列表包含（主题，纯文本正文部分，html的正文部分，发件人元组，收件人元组，附件列表）
    '''

    def get_mail_info(self, num):
        msg = self.get_email_format(num)
        attachments = []
        body = None
        html = None
        for part in msg.walk():
            attachment = self.parse_attachment(part)
            if attachment:
                attachments.append(attachment)
            elif part.get_content_type() == "text/plain":
                if body is None:
                    body = ""
                body += part.get_payload()
            elif part.get_content_type() == "text/html":
                if html is None:
                    html = ""
                html += part.get_payload()
        return {
            'id': msg['Message-ID'],
            'subject': self.get_subject_content(msg),
            'body': body,
            'html': html,
            'from': self.get_sender_info(msg),
            'to': self.get_receiver_info(msg),
            'date': self.get_date_info(msg),
            'attachments': attachments
        }
