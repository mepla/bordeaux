# -*- coding: UTF-8 -*-


import logging
import smtplib
from email.header import Header
from email.mime.text import MIMEText


class NotificationControllerBase(object):
    pass


class NotificationController(NotificationControllerBase):
    def __init__(self, notifiers):
        self._notifiers = notifiers

    def notify_new_items(self, new_items):
        map(lambda x: x.notify_new(new_items), self._notifiers)

    def notify_price_change(self, price_change_items):
        map(lambda x: x.notify_change_price(price_change_items), self._notifiers)


class NotifierBase(object):
    def notify_new(self, items):
        pass

    def notify_change_price(self, items):
        pass


class LogNotifier(NotifierBase):
    def __init__(self):
        pass

    def notify_new(self, items):
        logging.info('There are {} new items:'.format(len(items)))
        body = '\n'.join(map(lambda x: x.to_string(pretty=True, summarize=True), items))
        logging.info(body)

    def notify_change_price(self, items):
        logging.info('{} items has changed in price:'.format(len(items)))
        body = '\n'.join(map(lambda x: x.to_string(pretty=True, summarize=True), items))
        logging.info(body)


class EmailNotifier(NotifierBase):
    def __init__(self, email_configs):
        self._addr = email_configs.get('from_address')
        self._passw = email_configs.get('from_password')
        self._server = email_configs.get('smtp_server')
        self._port = email_configs.get('smtp_port')
        self._to = email_configs.get('to_address')
        self._send_mail(self._to, 'salam', u'سلاک')

    def _send_mail(self, to, subject, body):
        server = smtplib.SMTP(self._server, int(self._port))
        server.starttls()
        server.login(self._addr, self._passw)

        m = MIMEText(body.encode('utf-8'), 'plain', 'utf-8')
        m['Subject'] = Header(subject, 'utf-8')

        send_resp = server.sendmail(self._addr, to, m.as_string())
        server.quit()

    def notify_new(self, items):
        body = '\n'.join(map(lambda x: x.to_string(pretty=True, summarize=True), items))
        self._send_mail(self._to, 'New Items', body)

    def notify_change_price(self, items):
        body = '\n'.join(map(lambda x: x.to_string(pretty=True, summarize=True), items))
        self._send_mail(self._to, 'Price Change', body)
