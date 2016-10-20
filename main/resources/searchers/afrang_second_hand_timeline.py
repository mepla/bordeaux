# -*- coding: UTF-8 -*-
import logging
import re

import requests
import bs4
from bs4.element import Tag
from main.data_types.item import Item
from main.resources.searchers.base_searcher import BaseSearcher


class AfrangSecondHandTimelineSearcher(BaseSearcher):

    def start_search(self):
        results = []

        for i in range(1, 3):
            search_url = self.base_url.rstrip('/') + '?page={}'.format(i)
            logging.debug('Afrang timeline searching for page {}: {}'.format(i, search_url))
            result = requests.get(search_url)
            soup = bs4.BeautifulSoup(result.content, 'html.parser')
            all_divs = soup.find_all('div', {'class': 'row-box-item box-s-3'})
            for div in all_divs:
                g = self.create_item(div)
                if g:
                    results.append(g)

        return self._refine_items(results)

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

            try:
                desc_tag = div.find('div', {'class': 'desc-pro'}).p.next.strip()
                g.description = desc_tag
            except:
                g.description = ''

            return g
        except Exception as exc:
            print('Could not parse div: {} -> {}\n\n'.format(div, exc))
            pass

    def _refine_items(self, items):
        refined_items = []
        for item in items:
            desired_words = self.search_phrases
            desired_regex = '.*({}).*'.format('|'.join(desired_words))
            if re.match(desired_regex, item.name, flags=re.IGNORECASE) or re.match(desired_regex, item.description, flags=re.IGNORECASE):
                desired_regex = '.*(xf|xt|xe|xa|x-|x1|560|۵۶۰|{}).*'.format('|'.join(desired_words))
                if re.match(desired_regex, item.name, flags=re.IGNORECASE) or re.match(desired_regex, item.description,
                                                                                       flags=re.IGNORECASE):
                    refined_items.append(item)
                    continue

        return refined_items

if __name__ == '__main__':
    res = AfrangSecondHandTimelineSearcher('http://www.afrangdigital.com/Useds/-1', ['fujifilm', 'fuji', 'fujinon', 'فوجی', 'فوجی فیلم', 'yongnuo'], {}).start_search()
    for r in res:
        s = r.to_string(summarize=True)
        print s
