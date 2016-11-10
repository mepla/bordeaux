import datetime
from main.store.database_drivers import MongoDatabase, DatabaseRecordNotFound, DatabaseEmptyResult
from main.utils.general_utils import base64


class DatabaseController(object):
    def __init__(self, items_db):
        assert isinstance(items_db, MongoDatabase)
        self.db = items_db
        self.new_items = []
        self.price_change_items = []
        self.special_items = []

    def analayze_and_save(self, array_of_items):
        self.new_items = []
        self.price_change_items = []
        self.special_items = []
        for item in array_of_items:
            item.id = base64(item.link)
            item.last_update = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
            self._handle_item(item)
            if item.type == 'special_item':
                self._handle_special_item(item)

        return self.new_items, self.price_change_items, self.special_items

    def _handle_item(self, item):
        try:
            existing_doc = self.db.find_doc('id', item.id, 'item')
            item.addition_date = existing_doc.get('addition_date')
            item.price_history = existing_doc.get('price_history')
            if not item.price_history:
                item.price_history = [{'price': item.price, 'date': item.last_update}]

            last_price = item.price_history[-1].get('price')
            if last_price != item.price:
                price_diff = last_price - item.price
                if price_diff < 0:
                    change_percent = int(float(float(price_diff) / float(last_price)) * 100)
                else:
                    change_percent = -int(float(float(-price_diff) / float(last_price)) * 100)

                item.price_history.append({'price': item.price, 'date': item.last_update, 'change_percent': change_percent})
                self.price_change_items.append(item)

            self.db.delete('item', {'id': item.id})
            self.db.save(item.to_json(), 'item')

        except (DatabaseRecordNotFound, DatabaseEmptyResult):
            if item.type == 'special_item':
                pass
            else:
                item.addition_date = item.last_update
                item.price_history = [{'price': item.price, 'date': item.last_update}]
                self.db.save(item.to_json(), 'item')
                self.new_items.append(item)

    def _handle_special_item(self, item):
        try:
            existing_doc = self.db.find_doc('id', item.id, 'special_item')
            item.addition_date = existing_doc.get('addition_date')
            item.price_history = existing_doc.get('price_history')
            if not item.price_history:
                item.price_history = [{'price': item.price, 'date': item.last_update}]

            self.db.delete('special_item', {'id': item.id})
            self.db.save(item.to_json(), 'special_item')

        except (DatabaseRecordNotFound, DatabaseEmptyResult):
            item.addition_date = item.last_update
            item.price_history = [{'price': item.price, 'date': item.last_update}]
            self.db.save(item.to_json(), 'special_item')
            self.special_items.append(item)
