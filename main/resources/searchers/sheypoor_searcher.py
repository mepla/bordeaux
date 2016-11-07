# -*- coding: UTF-8 -*-
import logging
import re

import unidecode
from bs4.element import Tag
import bs4
import requests

from main.data_types.item import Item
from main.resources.searchers.base_searcher import BaseSearcher


class SheypoorSearcher(BaseSearcher):

    def start_search(self):
        results = []
        search_queries = list(self.search_phrases)
        for qry in search_queries:
            search_url = self.base_url + '?q={}&c=&r=8'.format(qry)
            logging.debug('Sheypoor searching for {}: {}'.format(qry, self.base_url))
            try:
                sheypoor_res = requests.get(search_url, timeout=10)
            except Exception as exc:
                logging.error('Sheypoor search failed to connect `{}`)'.format(qry))
                continue

            if not (200 <= sheypoor_res.status_code < 300):
                logging.error('Sheypoor search failed for `{}`: ({} -> {})'.format(qry, sheypoor_res.status_code, sheypoor_res.content))
                continue

            soup = bs4.BeautifulSoup(sheypoor_res.content, 'html.parser')
            sec = soup.find('section', id='serp')

            if not sec:
                logging.debug("No item found for sheypoor search: `{}`".format(qry))
                continue

            all_item_medium = sec.find_all('article', {'class': 'item-medium'})
            for item_tag in all_item_medium:
                item = self.create_item(item_tag, qry, search_url)
                if item:
                    results.append(item)

        return self._refine_items(results)

    def create_item(self, sec, search_phrase=None, search_url=None):
        assert isinstance(sec, Tag)
        g = Item()

        g.shop = 'sheypoor'
        g.search_phrase = search_phrase
        g.search_url = search_url
        g.is_second_hand = True
        g.description = ''

        try:
            content = sec.find('div', {'class': 'content'})
            a = content.find('h2').find('a')
            name = a.contents[0]
            link = a['href']
            strong = content.find_next('p').find_next('p')
            price = strong.find('strong').contents[0]
            price = price.replace(',', '')
            price = int(unidecode.unidecode(price)) * 10

            g.name = name.strip()
            g.link = link
            g.price = price

            return g

        except Exception as exc:
            # print('Could not parse sec: {} -> {}\n\n'.format(sec, exc))
            pass

    def _refine_items(self, items):
        refined_items = []
        for item in items:
            desired_regex = '.*(xf|xt|xe|xa|x-|x1).*'
            if re.search(ur'.*دوچرخه.*', item.name, flags=re.IGNORECASE) or re.search(ur'.*دوچرخه.*', item.description, flags=re.IGNORECASE):
                continue
            if re.search(desired_regex, item.name, flags=re.IGNORECASE) or re.search(desired_regex, item.description, flags=re.IGNORECASE):
                refined_items.append(item)
                continue
            if item.search_phrase not in ['fujifilm', 'fuji', 'fujinon', 'فوجی', 'فوجی فیلم']:
                refined_items.append(item)
                continue

        return refined_items


if __name__ == '__main__':
    res = SheypoorSearcher('http://www.sheypoor.com/search', ['fujifilm', 'fuji', 'fujinon', 'فوجی', 'فوجی فیلم'], {}).start_search()
    for r in res:
        s = r.to_string(summarize=True)
        print s
