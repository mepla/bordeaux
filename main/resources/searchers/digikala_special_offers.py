# -*- coding: UTF-8 -*-

import datetime
import os

import requests
import logging

from main.data_types.item import Item, SpecialItem
from main.resources.searchers.base_searcher import BaseSearcher


class DigikalaSpecialOfferSearch(BaseSearcher):

    def start_search(self):
        results = []

        search_url = self.base_url

        logging.debug('Digikala special searching for special items: {}'.format(search_url))
        result = requests.get(search_url)
        if 200 <= result.status_code < 300:
            item_docs = result.json().get('responses')[0].get('hits').get('hits')
            for item_doc in item_docs:
                results.append(self.create_item(item_doc.get('_source'), 'digikala_special_items', search_url))
        else:
            logging.debug('DK searching for {}: ({})\n{}'.format('digikala_special_items', result.status_code, result.raw))

        return results

    def create_item(self, item_doc, search_phrase=None, search_url=None):
        g = SpecialItem()
        try:
            g.shop = 'digikala_special'
            g.search_phrase = search_phrase
            g.search_url = search_url

            g.price = item_doc.get('Price') - item_doc.get('Discount', 0)
            g.discount = item_doc.get('Discount')
            g.old_price = item_doc.get('Price')
            g.discount_percent = int(float(float(g.discount) / float(g.old_price)) * 100)
            g.view_price = item_doc.get('MaxPrice')

            try:
                g.start_date = datetime.datetime.strptime(item_doc.get('StartDateTime'), '%Y-%m-%dT%H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
            except:
                g.start_date = datetime.datetime.strptime(item_doc.get('StartDateTime'), '%Y-%m-%dT%H:%M:%S.%f').strftime('%Y-%m-%d %H:%M:%S')

            try:
                g.end_date = datetime.datetime.strptime(item_doc.get('EndDateTime'), '%Y-%m-%dT%H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
            except:
                g.end_date = datetime.datetime.strptime(item_doc.get('EndDateTime'), '%Y-%m-%dT%H:%M:%S.%f').strftime('%Y-%m-%d %H:%M:%S')

            g.title = item_doc.get('ShowTitle')
            g.name = item_doc.get('EnTitle')
            g.is_second_hand = False

            g.image_link = os.path.join('http://file.digikala.com/Digikala', item_doc.get('ProductImagePath'))
            g.link = 'http://www.digikala.com/Product/DKP-{}'.format(item_doc.get('ProductId'))

            return g
        except Exception as exc:
            print('Could not parse item_doc: {} -> {}\n\n'.format(exc, item_doc))

if __name__ == '__main__':

    res = DigikalaSpecialOfferSearch("http://search.digikala.com/api2/Data/Get?categoryId=0&ip=0", [], {}).start_search()
    for r in res:
        s = r.to_string(summarize=True)
        print s
