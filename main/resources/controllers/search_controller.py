import importlib

from main.resources.controllers.database_controller import DatabaseController


class SearchController(object):
    def __init__(self, searchers_dict, database_controller):
        self.searchers = searchers_dict
        assert isinstance(database_controller, DatabaseController)
        self.database_controller = database_controller

    def start_search(self):
        aggregate_results = {}
        for searcher_name, searcher_data in self.searchers.items():
            module = importlib.import_module(searcher_data.get('module'))
            class_ = getattr(module, searcher_data.get('class'))
            instance = class_(searcher_data.get('base_url'), searcher_data.get('phrases'))
            instance_results = instance.start_search()
            for i in instance_results:
                print str(i)

            aggregate_results[searcher_name] = instance_results

        for name, result_array in aggregate_results.items():
            self.database_controller.analayze_and_save(result_array)