# -*- coding: UTF-8 -*-


import json


class Item(object):

    def __init__(self, data=None):
        self.price = None
        self.price_history = []
        self.view_price = None
        self.is_second_hand = None
        self.creation_date = None
        self.is_deleted = None
        self.deletion_date = None
        self.title = None
        self.link = None
        self.owner_details = None
        self.name = None
        self.description = None
        self.image_link = None
        self.is_read = False
        self.id = None
        self.search_phrase = None
        self.search_url = None
        self.shop = None
        self.last_update = None
        self.addition_date = None
        self.type = 'item'

        if data:
            attr_dict = dict(self.__dict__)
            for attr_key in attr_dict:
                if attr_key in data:
                    self.__dict__[attr_key] = data[attr_key]
                    # setattr(self, attr_key, data[attr_key])

    def to_json(self, summarize=False):
        try:
            if summarize is False:
                json_data = {}
                attr_dict = dict(self.__dict__)
                for attr_key, attr_value in attr_dict.items():
                    json_data[attr_key] = attr_value
            else:
                json_data = {
                    'name': self.name,
                    'shop': self.shop,
                    'price': self.price,
                    'link': self.link,
                    'addition_date': self.addition_date,
                    'search_phrase': self.search_phrase,
                    'price_history': self.price_history
                }

            return json_data
        except Exception as exc:
            pass

    def to_string(self, pretty=False, summarize=False):
        s = self.__str__(pretty=pretty, summarize=summarize)
        return s

    def __str__(self, pretty=False, summarize=False):
        json_data = self.to_json(summarize=summarize)

        try:
            for k, v in json_data.items():
                if isinstance(v, str):
                    json_data[k] = unicode(v, encoding='utf-8')

            if pretty is True:
                return json.dumps(json_data,
                                  ensure_ascii=False,
                                  indent=2,
                                  separators=(',', ': '))
            else:
                return json.dumps(json_data, ensure_ascii=False)

        except Exception as exc:
            pass


class SpecialItem(Item):
    def __init__(self, data=None):
        self.type = 'special_item'
        self.discount = None
        self.discount_percent = None
        self.old_price = None
        self.start_date = None
        self.end_date = None

        if data:
            attr_dict = dict(self.__dict__)
            for attr_key in attr_dict:
                if attr_key in data:
                    self.__dict__[attr_key] = data[attr_key]

    def to_json(self, summarize=False):
        json_data = super(SpecialItem, self).to_json(summarize)
        try:
            if summarize is False:
                json_data = {}
                attr_dict = dict(self.__dict__)
                for attr_key, attr_value in attr_dict.items():
                    json_data[attr_key] = attr_value
            else:
                json_data['discount'] = self.discount
                json_data['discount_percent'] = self.discount_percent
                json_data['old_price'] = self.old_price
                json_data['start_date'] = self.start_date
                json_data['end_date'] = self.end_date

            return json_data

        except Exception as exc:
            pass


if __name__ == '__main__':
    i = Item()
    print i.to_json()
