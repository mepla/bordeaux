from main import config
from main.data_types.item import Item
from main.store.database_drivers import MongoDatabase
from main.utils.general_utils import base64

if __name__ == '__main__':
    mongo_db = MongoDatabase(config.get('database').get('mongo'))

    all_digikala = mongo_db.find_doc('shop', 'digikala', 'item', limit=100)
    for item_doc in all_digikala:
        item = Item(data=item_doc)
        mongo_db.delete('item', {'id': item.id})
        item.link = '/'.join(item.link.split('/')[0:-1])
        item.id = base64(item.link)
        mongo_db.save(item.to_json(), 'item')

