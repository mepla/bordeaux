from main import config
from main.data_types.item import Item
from main.store.database_drivers import MongoDatabase

if __name__ == '__main__':
    mongo_db = MongoDatabase(config.get('database').get('mongo'))

    all_digikala = mongo_db.find_doc('shop', 'divar', 'item', limit=100)
    for item_doc in all_digikala:
        item = Item(data=item_doc)
        mongo_db.delete('item', {'id': item.id})
        item.price *= 10
        for price_doc in item.price_history:
            price_doc['price'] *= 10
        mongo_db.save(item.to_json(), 'item')

