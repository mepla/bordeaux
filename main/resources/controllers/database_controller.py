import datetime

from main.store.database_drivers import MongoDatabase, DatabaseRecordNotFound, DatabaseEmptyResult
from main.utils.general_utils import base64


class DatabaseController(object):
    def __init__(self, items_db):
        assert isinstance(items_db, MongoDatabase)
        self.db = items_db

    def analayze_and_save(self, array_of_items):
        for item in array_of_items:
            item.id = base64(item.link)
            item.last_update = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
            try:
                existing_doc = self.db.find_doc('id', item.id, 'item')
                item.addition_date = existing_doc.get('addition_date')
                self.db.delete('item', {'id': item.id})
                self.db.save(item.to_json(), 'item')

            except (DatabaseRecordNotFound, DatabaseEmptyResult):
                item.addition_date = item.last_update
                self.db.save(item.to_json(), 'item')

