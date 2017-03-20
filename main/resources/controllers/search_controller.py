# -*- coding: UTF-8 -*-
import importlib
import logging
import time
import json
from main.resources.controllers.database_controller import DatabaseController
from main.resources.controllers.notification_controller import NotificationControllerBase
from multiprocessing.pool import ThreadPool


class SearchController(object):
    def __init__(self, searchers_dict, database_controller, notification_controller):
        self.searchers = searchers_dict
        assert isinstance(database_controller, DatabaseController)
        self.database_controller = database_controller
        assert issubclass(notification_controller.__class__, NotificationControllerBase)
        self.notification_controller = notification_controller
        self.thread_pool = ThreadPool(len(self.searchers))
        self.aggregate_results = {}
        self.searcher_reports = {'searchers': {}}

    def start_search(self):
        total_start = time.time()
        total_phrases_count = 0
        total_searchers = 0

        logging.debug("\n*********** Bordeaux started running at: {} ***********\n".format(total_start))

        for searcher_name, searcher_data in self.searchers.items():
            enabled = searcher_data.get('enabled')
            if enabled is not True:
                logging.debug('Searcher `{}` is disabled, skipping...'.format(searcher_name))
                continue
            module = importlib.import_module(searcher_data.get('module'))
            class_ = getattr(module, searcher_data.get('class'))
            phrases = searcher_data.get('phrases', [])
            total_phrases_count += len(phrases) or 1
            total_searchers += 1
            instance = class_(searcher_data.get('base_url'), phrases, searcher_name, searcher_data)
            searcher_start_time = time.time()
            self.searcher_reports['searchers'][searcher_name] = {'start_time': searcher_start_time, 'searches_performed': len(phrases) or 1}
            self.thread_pool.apply_async(instance.start_search, callback=self.searcher_finished)

        self.thread_pool.close()
        self.thread_pool.join()

        self.searcher_reports['total_time'] = time.time() - total_start
        self.searcher_reports['total_searchers'] = total_searchers
        self.searcher_reports['total_searches_performed'] = total_phrases_count

        all_new_items = []
        all_price_changes = []
        all_special_items = []
        for name, result_array in self.aggregate_results.items():
            new_items, price_change_items, special_items = self.database_controller.analayze_and_save(result_array)
            all_new_items.extend(new_items)
            all_price_changes.extend(price_change_items)
            all_special_items.extend(special_items)

        if len(all_new_items) > 0:
            self.notification_controller.notify_new_items(all_new_items)

        if len(all_price_changes) > 0:
            self.notification_controller.notify_price_change(all_price_changes)

        if len(all_special_items) > 0:
            self.notification_controller.notify_special_items(all_special_items)

        logging.debug("\n*********** Bordeaux finished running ***********\n\nREPORT: \n{}\n".format(json.dumps(self.searcher_reports, indent=4, sort_keys=True)))

    def searcher_finished(self, result):
        searcher_name, result_data = result
        self.searcher_reports['searchers'][searcher_name]['total_time'] = time.time() - self.searcher_reports['searchers'][searcher_name]['start_time']
        del self.searcher_reports['searchers'][searcher_name]['start_time']
        self.aggregate_results[searcher_name] = result_data
