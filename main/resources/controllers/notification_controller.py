import logging
import smtplib


class NotificationControllerBase(object):
    pass


class NotificationController(NotificationControllerBase):
    def __init__(self, notifiers):
        self._notifiers = notifiers

    def notify_new_items(self, new_items):
        map(lambda x: x.notify(new_items), self._notifiers)


class NotifierBase(object):
    def notify(self, items):
        pass


class LogNotifier(NotifierBase):
    def __init__(self):
        pass

    def notify(self, items):
        logging.info('There are {} new items:'.format(len(items)))
        body = '\n'.join(map(lambda x: x.to_string(pretty=True, summarize=True), items))
        logging.info(body)


class EmailNotifier(NotifierBase):
    def __init__(self, email_configs):
        self._addr = email_configs.get('from_address')
        self._passw = email_configs.get('from_password')
        self._server = email_configs.get('smtp_server')
        self._port = email_configs.get('smtp_port')
        self._to = email_configs.get('to_address')

    def _send_mail(self, to, subject, body):
        server = smtplib.SMTP(self._server, int(self._port))
        server.starttls()
        server.login(self._addr, self._passw)
        body = 'Subject: {}\n\n{}'.format(subject, body)
        send_resp = server.sendmail(self._addr, to, body)
        server.quit()

    def notify(self, items):
        body = '\n'.join(map(lambda x: x.to_string(pretty=True, summarize=True), items))
        self._send_mail(self._to, 'New Items', body)
