from main.resources.searchers.afrang_second_hand import AfrangSecondHandSearcher

if __name__ == '__main__':
    ar = AfrangSecondHandSearcher(base_url='http://www.afrangdigital.com', phrases=['fujinon', 'fujifilm', 'xf 5', 'xf 1', 'xf 6', 'xf 9'])
    ar.start_search()