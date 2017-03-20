# -*- coding: UTF-8 -*-
import importlib
import logging
import time
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

    def start_search(self):
        start = time.time()
        for searcher_name, searcher_data in self.searchers.items():
            enabled = searcher_data.get('enabled')
            if enabled is not True:
                logging.debug('Searcher `{}` is disabled, skipping...'.format(searcher_name))
                continue
            module = importlib.import_module(searcher_data.get('module'))
            class_ = getattr(module, searcher_data.get('class'))
            instance = class_(searcher_data.get('base_url'), searcher_data.get('phrases', []), searcher_name, searcher_data)

            self.thread_pool.apply_async(instance.start_search, callback=self.searcher_finished)

        self.thread_pool.close()
        self.thread_pool.join()

        print time.time() - start
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

    def searcher_finished(self, result):
        searcher_name, result_data = result
        self.aggregate_results[searcher_name] = result_data
