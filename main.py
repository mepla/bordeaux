import argparse
import logging
import traceback

import sys

from main.resources.controllers.database_controller import DatabaseController
from main.resources.controllers.notification_controller import NotificationController, EmailNotifier, LogNotifier
from main.resources.controllers.search_controller import SearchController
from main import config
from main.resources.reporters.general_reporter import ReporterFactory
from main.store.database_drivers import MongoDatabase

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    required_group = parser.add_argument_group('Report info')
    required_group.add_argument('-r', action='store_true', dest='report', help='report', default=False, required=False)

    results = parser.parse_args()

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

    try:
        if not results.report:

            mongo = MongoDatabase(config.get('database').get('mongo'))
            dc = DatabaseController(mongo)

            en = EmailNotifier(config.get('notifiers').get('email'))
            ln = LogNotifier()

            nc = NotificationController([ln, en])

            sc = SearchController(config.get('searchers'), dc, nc)
            sc.start_search()
        else:
            mongo = MongoDatabase(config.get('database').get('mongo'))
            reporter = ReporterFactory(mongo, results).get_reporter()
            reporter.report()

    except Exception as exc:
        notifier = EmailNotifier(config.get('notifiers').get('email'))
        exception_formatted = traceback.print_exc(file=sys.stderr)
        logging.critical(exception_formatted)
        notifier.send_mail(None, 'Exception in bordeaux ({} -> {})'.format(type(exc), exc), exception_formatted)

