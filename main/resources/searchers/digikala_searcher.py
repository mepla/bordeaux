# -*- coding: UTF-8 -*-

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

            search_url = '{}/?category={}&status=2&pageSize=100'.format(self.base_url, categories.get(cat).get('category'))

            attribs = categories.get(cat).get('attributes')
            if attribs:
                search_url += '&attribute={}'.format(' '.join(attribs))

            brand = categories.get(cat).get('brand')
            if brand:
                search_url += '&brand={}'.format(brand)

            q_type = categories.get(cat).get('type')
            if q_type:
                search_url += '&type={}'.format(q_type)

            logging.debug('Digikala searching for {}: {}'.format(cat, search_url))
            try:
                result = requests.get(search_url, timeout=10)
            except Exception as exc:
                logging.error('Digikala search failed to connect `{}`)'.format(cat))
                continue

            if not (200 <= result.status_code < 300):
                logging.error('Digikala search failed for `{}`: ({} -> {})'.format(cat, result.status_code, result.content))
                continue

            item_docs = result.json().get('hits').get('hits')
            for item_doc in item_docs:
                item = self.create_item(item_doc.get('_source'), cat, search_url)
                if item:
                    results.append(item)

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
            g.link = 'http://www.digikala.com/Product/DKP-{}'.format(item_doc.get('Id'))

            return g

        except Exception as exc:
            print('Could not parse item_doc: {} -> {}\n\n'.format(exc, item_doc))
