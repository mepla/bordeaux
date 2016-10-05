import pymongo
import logging
import time
from pymongo import MongoClient

from main.utils.general_utils import filter_general_document_db_record


class DatabaseFindError(Exception):
    pass


class DatabaseSaveError(Exception):
    pass


class DatabaseRecordNotFound(Exception):
    pass


class DocumentNotUpdated(Exception):
    pass


class DatabaseNotFound(Exception):
    pass


class DatabaseEmptyResult(Exception):
    pass


class GraphDatabaseBase(object):
    pass


class DocumentDatabaseBase(object):
    pass


class MongoDatabase(DocumentDatabaseBase):
    def __init__(self, host='localhost', port=27017, db='items'):

        self._mongo_client = MongoClient(host, port)
        if db == 'items':
            self._mongo_db = self._mongo_client.items
        else:
            raise DatabaseNotFound('The database you requested was not found: {}'.format(db))

    def save(self, doc, doc_type, multiple=False):
        if not doc_type:
            raise DatabaseSaveError('No doc_type provided.')

        try:
            if multiple:
                objs = self._mongo_db[doc_type].insert_many(doc, ordered=False)
            else:
                obj = self._mongo_db[doc_type].insert_one(doc)
        except Exception as exc:
            logging.error('Error saving doc to database: {} exc: {}'.format(self._mongo_db, exc))
            raise DatabaseSaveError()

    def delete(self, doc_type, conditions, multiple=False):
        if multiple:
            result = self._mongo_db[doc_type].delete_many(conditions)
        else:
            result = self._mongo_db[doc_type].delete_one(conditions)

        return result.deleted_count

    def find_doc(self, key, value, doc_type, limit=1, conditions=None, sort_key=None, sort_direction=1):
        try:
            find_predicate = {}
            if conditions:
                find_predicate = conditions

            if key and value:
                find_predicate[key] = value

            if limit == 1:
                doc = self._mongo_db[doc_type].find_one(find_predicate)
                if not doc:
                    raise DatabaseRecordNotFound()
                return doc
            else:
                if sort_key:
                    directon = pymongo.DESCENDING if sort_direction == -1 else pymongo.ASCENDING
                    cursor = self._mongo_db[doc_type].find(find_predicate, limit=limit).sort(sort_key, directon)
                else:
                    cursor = self._mongo_db[doc_type].find(find_predicate, limit=limit)
                return_list = []
                for doc in cursor:
                    return_list.append(filter_general_document_db_record(doc))
                if len(return_list) < 1:
                    raise DatabaseEmptyResult()
                return return_list

        except DatabaseRecordNotFound as exc:
            raise exc

        except DatabaseEmptyResult as exc:
            raise exc

        except Exception as exc:
            logging.error('Error in finding doc in database: {} exc: {}'.format(self._mongo_db, exc))
            raise DatabaseFindError()
