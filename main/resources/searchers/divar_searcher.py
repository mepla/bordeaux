# -*- coding: UTF-8 -*-
import logging
import re

import requests

from main.data_types.item import Item
from main.resources.searchers.base_searcher import BaseSearcher, ThreadedSearcher


class DivarSearcher(ThreadedSearcher):

    def _post_params(self, qry):
        return {
            "jsonrpc": "2.0",
            "method": "getPostList",
            "id": 1,
            "params": [
                [
                    ["place2", 0, ["1"]],
                    ["query", 0, [qry]]
                ], 0
            ]
        }

    def start_search(self):
        search_queries = list(self.search_phrases)
        for qry in search_queries:
            self.do_the_job(self.perform_search_query, (qry,))

        return self.return_results(self._refine_items)

    def perform_search_query(self, qry):
        local_all_results = []
        post_param = self._post_params(qry)
        logging.debug('Divar searching for {}: {}'.format(qry, self.base_url))

        try:
            result = requests.post(self.base_url, json=post_param, timeout=10)
        except Exception as exc:
            logging.error('Divar search failed to connect `{}`)'.format(qry))
            return []

        if not (200 <= result.status_code < 300):
            logging.error(
                'Divar search failed for `{}`: ({} -> {})'.format(self.base_url, result.status_code, result.content))
            return []

        res_array = result.json().get('result').get('post_list')
        for item_doc in res_array:
            item = self.create_item(item_doc, qry, self.base_url)
            if item:
                local_all_results.append(item)

        return local_all_results

    def create_item(self, item_doc, search_phrase=None, search_url=None):
        g = Item()

        try:
            g.shop = 'divar'
            g.name = item_doc.get('title')
            g.title = item_doc.get('title')
            g.description = item_doc.get('desc')
            g.price = item_doc.get('v09')
            if g.price and g.price > 0:
                g.price *= 10
            g.search_phrase = search_phrase
            g.search_url = search_url
            g.is_second_hand = True
            g.link = u'https://divar.ir/v/' + unicode(item_doc.get('title')) + '/' + item_doc.get('token')

            return g
        except Exception as exc:
            print('Could not parse item_doc: {} -> {}\n\n'.format(exc, item_doc))

    def _refine_items(self, items):
        refined_items = []
        for item in items:
            if not item:
                continue
            desired_regex = '.*(xf|xt|xe|xa|x-|x1).*'
            if re.search(ur'.*دوچرخه.*', item.name, flags=re.IGNORECASE) or re.search(ur'.*دوچرخه.*', item.description, flags=re.IGNORECASE and re.MULTILINE):
                continue
            if re.search(desired_regex, item.name, flags=re.IGNORECASE) or re.search(desired_regex, item.description, flags=re.IGNORECASE and re.MULTILINE):
                refined_items.append(item)
                continue
            if item.search_phrase not in ['fujifilm', 'fuji', 'fujinon', 'فوجی', 'فوجی فیلم']:
                refined_items.append(item)
                continue

        return refined_items


if __name__ == '__main__':
    res = DivarSearcher('https://search.divar.ir/json/', ['fujifilm', 'fuji', 'fujinon', 'فوجی', 'فوجی فیلم', 'yongnuo'], {}).start_search()
    for r in res:
        s = r.to_string(summarize=True)
        print s
