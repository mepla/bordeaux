# -*- coding: UTF-8 -*-

import requests
import bs4
from bs4.element import Tag
from main.data_types.item import Item
from main.resources.searchers.base_searcher import BaseSearcher


class AfrangSecondHandSearcher(BaseSearcher):

    def start_search(self):
        results = []

        search_queries = list(self.search_phrases)

        for qry in search_queries:
            search_url = '{}?Query={}'.format(self.base_url, qry)
            result = requests.get(search_url)
            soup = bs4.BeautifulSoup(result.content, 'html.parser')
            all_divs = soup.find_all('div')
            for div in all_divs:
                g = self.create_item(div)
                if g and g.link not in results:
                    results.append(g)

        return results

    def create_item(self, div, search_phrase=None, search_url=None):
        g = Item()
        g.shop = 'afrang'
        g.search_phrase = search_phrase
        g.search_url = search_url
        g.is_second_hand = True

        try:
            a_tag = div.find('div', {'class': 'name-pro2'}).h2.a
            assert isinstance(a_tag, Tag)
            tag_str = str(a_tag)
            link = tag_str[tag_str.index('"')+1:tag_str.rindex('"')]
            g.link = 'http://www.afrangdigital.com' + link

            title = tag_str[tag_str.index('">')+2:-4]
            g.title = title
            g.name = title

            price_tag = div.find('span', {'class': 'price-pro'}).price
            price_str = str(price_tag)
            g.view_price = price_str
            price_str = price_str.split(' ')[0].replace('<price>', '').replace(',', '')
            g.price = price_str

            return g
        except Exception as exc:
            # print('Could not parse div: {} -> {}\n\n'.format(div, exc))
            pass

if __name__ == '__main__':
    res = AfrangSecondHandSearcher('', ['test'], {}).start_search()
    for r in res:
        s = r.to_string(summarize=True)
        print s
