import datetime
import os

import requests
import logging

from main.data_types.item import Item
from main.resources.searchers.base_searcher import BaseSearcher


class DigikalaSearcher(BaseSearcher):

    def start_search(self):
        results = []
        search_queries = list(self.search_phrases)

        categories = self.searcher_conf.get('phrase_details')

        for cat in search_queries:
            if cat not in categories:
                logging.warn('There is no defined category in Digikala for: {}, Skipping...'.format(cat))
                continue

            search_url = '{}/?category={}&status=2&type={}&pageSize=100'.format(self.base_url, categories.get(cat).get('category'), categories.get(cat).get('type'))
            logging.debug('DK searching for {}: {}'.format(cat, search_url))
            result = requests.get(search_url)
            if 200 <= result.status_code < 300:
                item_docs = result.json().get('hits').get('hits')
                for item_doc in item_docs:
                    results.append(self.create_item(item_doc.get('_source'), cat, search_url))
            else:
                logging.debug('DK searching for {}: ({})\n{}'.format(cat, result.status_code, result.raw))

        return results

    def create_item(self, item_doc, search_phrase=None, search_url=None):
        g = Item()
        try:
            g.shop = 'digikala'
            g.search_phrase = search_phrase
            g.search_url = search_url

            g.price = item_doc.get('MinPrice')
            g.view_price = item_doc.get('MaxPrice')
            try:
                g.creation_date = datetime.datetime.strptime(item_doc.get('RegDateTime'), '%Y-%m-%dT%H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
            except:
                g.creation_date = datetime.datetime.strptime(item_doc.get('RegDateTime'), '%Y-%m-%dT%H:%M:%S.%f').strftime('%Y-%m-%d %H:%M:%S')
            g.title = item_doc.get('FaTitle')
            g.name = item_doc.get('EnTitle')
            g.image_link = os.path.join('http://file.digikala.com/Digikala', item_doc.get('ImagePath'))
            g.is_second_hand = False
            g.link = os.path.join('http://www.digikala.com/Product/DKP-{}'.format(item_doc.get('Id')), item_doc.get('UrlCode'))

            return g
        except Exception as exc:
            print('Could not parse item_doc: {} -> {}\n\n'.format(exc, item_doc))
