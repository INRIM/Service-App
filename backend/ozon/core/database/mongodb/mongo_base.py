# Copyright INRIM (https://www.inrim.eu)
# See LICENSE file for full licensing details.
import sys
from app import config

from datetime import datetime, timedelta
import bson
from odmantic import AIOEngine
from odmantic.engine import AIOCursor
import logging
import pymongo
from pymongo import ReadPreference
from motor.motor_asyncio import AsyncIOMotorClient

from .base_model import *
import ujson

logger = logging.getLogger(__name__)

settings = config.SettingsApp()

# client = AsyncIOMotorClient(
#     settings.mongo_url,
#     username=settings.mongo_user,
#     password=settings.mongo_pass,
#     replicaset=settings.mongo_replica,
#     # tz_aware=True,
#     serverSelectionTimeoutMS=10, connectTimeoutMS=20000)

mongocfg = f"mongodb://{settings.mongo_user}:{settings.mongo_pass}" \
           f"@{settings.mongo_url}"

client = AsyncIOMotorClient(
    mongocfg,
    replicaset=settings.mongo_replica,
    connectTimeoutMS=30000, socketTimeoutMS=None, socketKeepAlive=True, connect=False, maxPoolsize=3,
    serverSelectionTimeoutMS=10)

engine = AIOEngine(motor_client=client, database=settings.mongo_db)


# TODO handle update schema to test
# db.foo.updateMany( {}, <update> )
# db.foo.updateMany({"created": false}, {"$set":{"created": true}});
# motor
# await coll.update_many({'i': {'$gt': 100}},
#                        {'$set': {'key': 'value'}})

## TODO helper function
def _data_helper(d):
    if isinstance(d, bson.objectid.ObjectId) or isinstance(d, datetime):
        return str(d)

    if isinstance(d, list):  # For those db functions which return list
        return [_data_helper(x) for x in d]

    if isinstance(d, dict):
        for k, v in d.items():
            d.update({k: _data_helper(v)})

    # return anything else, like a string or number
    return d


def data_helper(d):
    d = _data_helper(d)
    return d


def get_data_list(
        list_data, fields=[], merge_field="", row_action="",
        additional_key=[], remove_keys=[]):
    new_list = []
    for i in list_data:
        if not isinstance(i, dict):
            data = ujson.loads(i.json())
        else:
            data = data_helper(i)
        if row_action:
            data['row_action'] = f"{row_action}/{data['rec_name']}"
        if additional_key:
            data[additional_key[0]] = data[additional_key[1]]
        if remove_keys:
            for k, v in data.items():
                if isinstance(v, dict):
                    for k1 in remove_keys:
                        if k1 in v:
                            v.pop(k1)
            for k in remove_keys:
                if k in data:
                    data.pop(k)
        new_list.append(data_helper_list(
            data, fields=fields, merge_field=merge_field))
    return new_list


def data_helper_list(d, fields=[], merge_field=""):
    dres = {}
    data = d
    if fields:
        dres = {}
        if merge_field:
            for k in fields:
                if not k == merge_field:
                    data[merge_field][k] = data.get(k)
            res = data[merge_field].copy()
            return res
        else:
            for k in fields:
                dres[k] = data.get(k)
            return dres
    else:
        return data


async def set_unique(schema: Type[ModelType], field_name):
    component_coll = engine.get_collection(schema)
    await component_coll.create_index([(field_name, 1)], unique=True)


async def prepare_collenctions():
    await set_unique(Component, "rec_name")
    await set_unique(Component, "title")


async def get_collections_names(query={}):
    if not query:
        query = {"name": {"$regex": r"^(?!system\.)"}}
    collection_names = await engine.database.list_collection_names(filter=query)
    return collection_names


## TODO handle records
async def search_distinct(model: Type[ModelType], distinct="rec_name", clausole={}):
    coll = engine.get_collection(model)
    values = await coll.distinct(distinct, clausole)
    return values


async def search_by_filter(schema: Type[ModelType], domain: dict, sort: list = [], limit=0, skip=0):
    logger.info(
        f"search_by_filter: schema:{schema}, domain:{domain}, sort:{sort}, limit:{limit}, skip:{skip}")
    coll = engine.get_collection(schema)
    if limit > 0:
        datas = await coll.find(domain).sort(sort).skip(skip).limit(limit).to_list(None)
    else:
        datas = await coll.find(domain).sort(sort).to_list(None)

    return datas


async def aggregate(schema: Type[ModelType], pipeline: dict, sort: list = [], limit=0, skip=0):
    logger.info(
        f"aggregate: schema:{schema}, pipeline:{type(domain)}, sort:{sort}, limit:{limit}, skip:{skip}")
    coll = engine.get_collection(schema)
    if limit > 0:
        datas = await coll.aggregate(pipeline).sort(sort).skip(skip).limit(limit).to_list(None)
    else:
        datas = await coll.aggregate(pipeline).sort(sort).to_list(None)

    return datas


async def count_by_filter(schema: Type[ModelType], domain: dict) -> int:
    logger.info(f"count_by_filter: schema")
    coll = engine.get_collection(schema)
    val = await coll.count_documents(domain)
    if not val:
        val = 0
    # val = res.count(True)
    return int(val)


async def search_all(model: Type[ModelType], sort: list = [], limit=0, skip=0) -> List[ModelType]:
    datas = await search_by_filter(model, {}, sort=sort)
    return datas


async def search_all_distinct(
        model: Type[ModelType], distinct="", query={}, compute_label="", sort: list = []) -> List[ModelType]:
    logger.info("search_all_distinct")
    coll = engine.get_collection(model)
    if not query:
        query = {"deleted": 0}
    label = {"$first": f"$title"}
    label_lst = compute_label.split(",")
    if compute_label:
        if len(label_lst) > 0:
            block = []
            for item in label_lst:
                if len(block) > 0:
                    block.append(f" - ")
                block.append(f"${item}")
            label = {"$first": {"$concat": block}}

        else:
            label = {"$first": f"${label_lst[0]}"}

    pipeline = [
        {"$match": query},
        {
            "$group":
                {
                    "_id": "$_id",
                    f"{distinct}": {"$first": f"${distinct}"},
                    "title": label,
                    "type": {"$first": f"$type"}
                }
        },
        {'$sort': {'title': 1}}
    ]
    res = await coll.aggregate(pipeline).to_list(length=None)
    return res


async def search_by_type(schema: Type[ModelType], model_type: str, sort: Optional[Any] = None) -> List[ModelType]:
    query = (schema.type == model_type) & (schema.deleted == 0)
    if not sort:
        sort = [("list_order", pymongo.ASCENDING), ("rec_name", pymongo.ASCENDING)]
    datas = await engine.find(
        schema, query, sort=(schema.list_order, schema.rec_name.asc()))
    return datas


# Retrieve a form with a matching ID
async def search_by_id(schema: Type[ModelType], rec_id: str) -> Type[ModelType]:
    data = await engine.find_one(schema, schema.id == ObjectId(rec_id))
    if data:
        return data
    else:
        return False


async def search_by_name(schema: Type[ModelType], rec_name: str):
    data = await engine.find_one(schema, schema.rec_name == rec_name)
    if data:
        return data
    else:
        return False


async def search_by_uid(schema: Type[ModelType], rec_name: str):
    data = await engine.find_one(schema, schema.uid == rec_name)
    if data:
        return data
    else:
        return False


async def save_record(schema):
    if isinstance(schema, Model):
        return await engine.save(schema)
    else:
        logger.warning(f"schema is {type(schema)}")


async def save_all(list_data):
    return await engine.save_all(list_data)


## TODO delete handler

async def delete_record(schema: Type[ModelType], rec_name: str):
    rec = await search_by_name(schema, rec_name)
    return await engine.delete(rec)


async def set_to_delete_records(schema: Type[ModelType], query={}):
    coll = engine.get_collection(schema)
    records = await coll.find(query).to_list(None)
    for rec in records:
        rec['id'] = rec['_id']
        record = schema(**rec)
        delete_at_datetime = datetime.now() + timedelta(days=settings.delete_record_after_days)
        record.deleted = delete_at_datetime.timestamp()
        await engine.save(record)
    return True


async def delete_records(schema: Type[ModelType], query={}):
    coll = engine.get_collection(schema)
    records = await coll.find(query).to_list(None)
    for rec in records:
        rec['id'] = rec['_id']
        record = schema(**rec)
        await engine.delete(record)
    return True


async def set_to_delete_record(schema: Type[ModelType], rec):
    delete_at_datetime = datetime.now() + timedelta(days=settings.delete_record_after_days)
    rec.deleted = delete_at_datetime.timestamp()
    return await engine.save(rec)


async def retrieve_all_to_delete(schema: Type[ModelType]):
    curr_timestamp = datetime.now().timestamp()
    res = await engine.find(schema, schema.deleted >= curr_timestamp)
    return res


async def erese_all_to_delete_record(schema: Type[ModelType], rec_id: str):
    res = await retrieve_all_to_delete(schema)
    for rec in res:
        await engine.delete(rec)
    return True


async def erese_to_delete_record(record: Type[ModelType]):
    await engine.delete(record)
    return True


## TODO handle archiviations

async def retrieve_all_archivied(schema: Type[ModelType]):
    res = await engine.find(schema, schema.active == False)
    return res


async def set_active(schema: Type[ModelType], rec_id: str):
    rec = await search_by_id(schema, rec_id)
    rec.active = True
    return await engine.save(rec)


async def set_archivied(schema: Type[ModelType], rec_id: str):
    rec = await search_by_id(schema, rec_id)
    rec.active = False
    return await engine.save(rec)


# TODO handle collections index

async def get_collection_index_fields(schema):
    logger.info("get_collection_index_fields")
    coll = engine.get_collection(schema)
    fields = []
    async for index in coll.list_indexes():
        item = data_helper(index)
        fields.append(item)
    return fields
