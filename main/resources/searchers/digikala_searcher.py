# -*- coding: UTF-8 -*-

import datetime
import os
import math
import requests
import logging

from main.data_types.item import Item
from main.resources.searchers.base_searcher import ThreadedSearcher, BaseSearcher


class DigikalaSearcher(ThreadedSearcher):

    def start_search(self):
        search_queries = list(self.search_phrases)

        for cat in search_queries:
            self.do_the_job(self.perform_search_query, (cat,))

        return self.return_results()

    def perform_search_query(self, cat):
        local_all_results = []
        categories = self.searcher_conf.get('phrase_details')
        if cat not in categories:
            logging.warn('There is no defined category in Digikala for: {}, Skipping...'.format(cat))
            return []

        page_no = 0
        page_size = 100
        search_url = '{}/?category={}&status=2&pageSize={}&pageno={}'.format(self.base_url,
                                                                             categories.get(cat).get('category'),
                                                                             page_size, page_no)

        attribs = categories.get(cat).get('attributes')
        if attribs:
            for attr in attribs:
                search_url += '&attribute={}'.format(attr)

        brand = categories.get(cat).get('brand')
        if brand:
            search_url += '&brand={}'.format(brand)

        q_type = categories.get(cat).get('type')
        if q_type:
            search_url += '&type={}'.format(q_type)

        page_results, page_count, total_count = self.search_and_add(search_url, cat)
        if not total_count:
            return []

        local_all_results.extend(page_results)

        further_pages = int(math.ceil(float(total_count) / float(page_count)))
        for i in range(1, further_pages):
            search_url = search_url.replace('pageno={}'.format(i - 1), 'pageno={}'.format(i))
            page_results, page_count, total_count = self.search_and_add(search_url, cat)
            local_all_results.extend(page_results)

        return local_all_results

    def search_and_add(self, search_url, cat):
        results = []
        logging.debug('Digikala searching for {}: {}'.format(cat, search_url))
        try:
            result = requests.get(search_url, timeout=10)
        except Exception as exc:
            logging.error('Digikala search failed to connect `{}`)'.format(cat))
            return [], 0, None

        if not (200 <= result.status_code < 300):
            logging.error('Digikala search failed for `{}`: ({} -> {})'.format(cat, result.status_code, result.content))
            return [], 0, None

        item_docs = result.json().get('hits').get('hits')
        items_count = len(item_docs)
        total_count = result.json().get('hits').get('total')
        for item_doc in item_docs:
            item = self.create_item(item_doc.get('_source'), cat, search_url)
            if item:
                results.append(item)

        return results, items_count, total_count

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
