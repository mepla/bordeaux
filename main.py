import logging

from main.resources.controllers.database_controller import DatabaseController
from main.resources.controllers.search_controller import SearchController
from main import config
from main.store.database_drivers import MongoDatabase

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

    mongo = MongoDatabase()
    dc = DatabaseController(mongo)

    sc = SearchController(config.get('searchers'), dc)
    sc.start_search()
