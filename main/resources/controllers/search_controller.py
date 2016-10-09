import importlib
import logging

from main.resources.controllers.database_controller import DatabaseController
from main.resources.controllers.notification_controller import NotificationControllerBase


class SearchController(object):
    def __init__(self, searchers_dict, database_controller, notification_controller):
        self.searchers = searchers_dict
        assert isinstance(database_controller, DatabaseController)
        self.database_controller = database_controller
        assert issubclass(notification_controller.__class__, NotificationControllerBase)
        self.notification_controller = notification_controller

    def start_search(self):
        aggregate_results = {}
        for searcher_name, searcher_data in self.searchers.items():
            enabled = searcher_data.get('enabled')
            if enabled is not True:
                logging.debug('Searcher `{}` is disabled, skipping...'.format(searcher_name))
                continue
            module = importlib.import_module(searcher_data.get('module'))
            class_ = getattr(module, searcher_data.get('class'))
            instance = class_(searcher_data.get('base_url'), searcher_data.get('phrases'), searcher_data)
            instance_results = instance.start_search()

            aggregate_results[searcher_name] = instance_results

        all_new_items = []
        all_price_changes = []
        for name, result_array in aggregate_results.items():
            new_items, price_change_items = self.database_controller.analayze_and_save(result_array)
            all_new_items.extend(new_items)
            all_price_changes.extend(price_change_items)

        if len(all_new_items) > 0:
            self.notification_controller.notify_new_items(all_new_items)

        if len(all_price_changes) > 0:
            self.notification_controller.notify_price_change(all_price_changes)