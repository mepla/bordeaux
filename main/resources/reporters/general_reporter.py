from main.data_types.item import Item
from main.store.database_drivers import MongoDatabase


class ReporterDoesNotExist(Exception):
    pass


class ReporterFactory(object):
    def __init__(self, items_db, cl_args):
        self.db = items_db
        self.args = cl_args

    def get_reporter(self):
        if self.args.report:
            return LastItemsReporter(self.db)
        else:
            raise ReporterDoesNotExist()


class BaseReporter(object):
    pass


class LastItemsReporter(BaseReporter):
    def __init__(self, items_db):
        assert isinstance(items_db, MongoDatabase)
        self.db = items_db

    def report(self):
        results = self.db.find_doc(None, None, 'item', sort_key='addition_date', sort_direction=-1, limit=10)
        results.reverse()
        for i, res in enumerate(results):
            title_number = len(results) - i
            item = Item(data=res)
            print '\n{} {} {}'.format('#'*10, title_number, '#'*10)
            print item.to_string(True, True)
