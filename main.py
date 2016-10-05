import logging

from main.resources.searchers.afrang_second_hand import AfrangSecondHandSearcher
from main.resources.searchers.digikala_searcher import DigikalaSearcher

if __name__ == '__main__':
    logger = logging.getLogger()

    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(lineno)s - %(process)d - %(threadName)s - %(message)s")
    handler.setFormatter(formatter)
    for hdl in logger.handlers:
        logger.removeHandler(hdl)
    logger.addHandler(handler)
    logger.addHandler(handler)
    logger.setLevel('DEBUG')

    ar = AfrangSecondHandSearcher(base_url='http://www.afrangdigital.com', phrases=['fujinon', 'fujifilm', 'xf 5', 'xf 1', 'xf 6', 'xf 9'])
    dk = DigikalaSearcher(base_url='http://search.digikala.com/api/search', phrases=['ps4_games'])
    dk.start_search()