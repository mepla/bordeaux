# -*- coding: UTF-8 -*-


import logging
import smtplib
from email.header import Header
from email.mime.text import MIMEText

from json2html import json2html


class NotificationControllerBase(object):
    pass


class NotificationController(NotificationControllerBase):
    def __init__(self, notifiers):
        self._notifiers = notifiers

    def notify_new_items(self, new_items):
        map(lambda x: x.notify_new(new_items), self._notifiers)

    def notify_price_change(self, price_change_items):
        map(lambda x: x.notify_change_price(price_change_items), self._notifiers)

    def notify_special_items(self, special_items):
        map(lambda x: x.notify_special_items(special_items), self._notifiers)


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

    def notify_special_items(self, items):
        logging.info('There are {} special items:'.format(len(items)))
        body = '\n'.join(map(lambda x: x.to_string(pretty=True, summarize=True), items))
        logging.info(body)


class EmailNotifier(NotifierBase):
    def __init__(self, email_configs):
        self._addr = email_configs.get('from_address')
        self._passw = email_configs.get('from_password')
        self._server = email_configs.get('smtp_server')
        self._port = email_configs.get('smtp_port')
        self._to = email_configs.get('to_address')
        self._change_percent_threshold = int(email_configs.get('change_percent_threshold', 10))

    def send_mail(self, to, subject, body=''):
        if not to:
            to = self._to

        server = smtplib.SMTP(self._server, int(self._port))
        server.starttls()
        server.login(self._addr, self._passw)

        if body.startswith('<html') or body.startswith('<table'):
            body_type = 'html'
        else:
            body_type = 'plain'
        m = MIMEText(body.encode('utf-8'), body_type, 'utf-8')
        m['Subject'] = Header(subject, 'utf-8')
        m['From'] = Header('Bordeaux Notification', 'utf-8')

        send_resp = server.sendmail(self._addr, to, m.as_string())
        server.quit()

    def notify_new(self, items):
        count = len(items)
        body = ''
        for item in items:
            data = item.to_json(summarize=True)
            if item.image_link:
                data['image'] = '<img src="{}" width=auto height=120 >'.format(item.image_link)
            html_doc = json2html.convert(json=data).replace('<li>', '').replace('</li>', '').replace('<ul>', '').replace('</ul>', '')
            body += u'{}<br> </br>'.format(html_doc)

        self.send_mail(self._to, '{} New Item{}'.format(count, 's' if count > 1 else ''), body)

    def notify_change_price(self, items):
        count = 0
        body = ''
        for item in items:
            data = item.to_json(summarize=True)
            try:
                last_percent = data.get('price_history')[-1].get('percent')
                if abs(int(last_percent)) < self._change_percent_threshold:
                    continue
            except:
                pass

            count += 1
            if item.image_link:
                data['image'] = '<img src="{}" width=auto height=120 >'.format(item.image_link)
            html_doc = json2html.convert(json=data).replace('<li>', '').replace('</li>', '').replace('<ul>', '').replace('</ul>', '')
            body += u'{}<br> </br>'.format(html_doc)

        if count:
            self.send_mail(self._to, '{} Price Change{}'.format(count, 's' if count > 1 else ''), body)

    def notify_special_items(self, items):
        count = len(items)
        body = ''
        for item in items:
            data = item.to_json(summarize=True)
            if item.image_link:
                data['image'] = '<a href="{}"> <img src="{}" width=auto height=120 > </a>'.format(item.link, item.image_link)
            html_doc = json2html.convert(json=data).replace('<li>', '').replace('</li>', '').replace('<ul>', '').replace('</ul>', '')
            body += u'{}<br> </br>'.format(html_doc)

        self.send_mail(self._to, '{} Special Item{}'.format(count, 's' if count > 1 else ''), body)
