import datetime
import os

import requests

from main.data_types.item import Item
from main.resources.searchers.base_searcher import BaseSearcher


class DivarSearcher(BaseSearcher):

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
        results = []
        search_queries = list(self.search_phrases)
        for qry in search_queries:
            post_param = self._post_params(qry)
            res = requests.post(self.base_url, json=post_param)
            res_array = res.json().get('result').get('post_list')
            for item_doc in res_array:
                item = self.create_item(item_doc, qry, self.base_url)
                results.append(item)
                print item.to_string(True, True)

    def create_item(self, item_doc, search_phrase=None, search_url=None):
        g = Item()

        try:
            g.shop = 'divar'
            g.name = item_doc.get('title')
            g.title = item_doc.get('title')
            g.description = item_doc.get('desc')
            g.price = item_doc.get('v09')
            g.search_phrase = search_phrase
            g.search_url = search_url
            g.is_second_hand = True
            g.link = os.path.join('https://divar.ir/v', item_doc.get('title'), item_doc.get('token'))

            return g
        except Exception as exc:
            print('Could not parse item_doc: {} -> {}\n\n'.format(exc, item_doc))

'''
{
			"v01": 1,
			"v09": 1750000,
			"hc": false,
			"c3": 32,
			"c2": 30,
			"ic": 1,
			"c1": 1,
			"c4": null,
			"p2": 1,
			"p3": null,
			"c": "11",
			"p1": null,
			"d": 29331,
			"p4": 78,
			"title": "Fujifilm X-Pro1",
			"p": 0,
			"token": "xMJdajJuD",
			"desc": "\u0628\u062f\u0646\u0647X-Pro1 \r\n\u062e\u06cc\u0644\u06cc \u062e\u06cc\u0644\u06cc \u06a9\u0645 \u06a9\u0627\u0631 \u06a9\u0631\u062f\u0647. \u062f\u0631 \u062d\u062f \u0622\u06a9\u0628\u0646\u062f. \u0628\u0627 \u06a9\u0627\u0631\u062a\u0646 \u0648 \u062a\u0645\u0627\u0645 \u0645\u062a\u0639\u0644\u0642\u0627\u062a..."
		}
'''

if __name__ == '__main__':
    DivarSearcher('https://search.divar.ir/json/', ['fujifilm'], {}).start_search()