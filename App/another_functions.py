# -*- coding: utf-8 -*-
import codecs
from datetime import datetime

import re
from pymongo import MongoClient
from bson.json_util import dumps, STRICT_JSON_OPTIONS
import os
from WebApp.settings import LOG_FILE_PATH

connection = MongoClient()

# Проверка строки лога на соответствие шаблону
def is_fine_line(line):
    return len(re.findall(r'(\[\d{4}\-\d{2}\-\d{2}\s\d{2}\:\d{2}\:\d{2}.\d{9}\+\d{2}\:\d{2}\])(\[\d+\])(\:.{1,})', line))

def razbor_stroki(line):
    #   разделяем по "]:" на две части
    parse_line = re.split(']\:',line)
    # извлекаем дату и pid из левой части
    parse_time = datetime.strptime(parse_line[0][1:27],'%Y-%m-%d %H:%M:%S.%f')
    parse_id = re.split('\]\[',parse_line[0])[1]
    # извлекаем событие из правой части, обрезаем символ конца строки
    parse_event = parse_line[1][:-1]
    return [parse_time, parse_id, parse_event]

def parsing():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    logpath = os.path.join(base_dir, LOG_FILE_PATH)
    logfile = codecs.open(logpath, "r", "utf_8_sig")
    # Построчный парсинг
    list_of_result_lists = []
    for line in logfile:
        if not is_fine_line(line):
            continue
        list_of_result_lists.append(razbor_stroki(line))
    return list_of_result_lists

def writing_into_database(results, coll):
    size_db = len(list(coll.find()))
    if (size_db != 0):
        last_date = coll.find()[size_db - 1].get("Time")
    if (size_db == 0 or last_date < results[0][0]):
        for elem in results:
            entry = {"Time": elem[0], "UID": elem[1], "Event": elem[2]}
            coll.insert(entry)

def get_collect(data_base = connection.local):
    collection = data_base.collect
    data_base.collect.create_index("Event")
    data_base.collect.create_index("Time")
    return collection

def pickup_from_database(data_base = connection.local, date_from='1015-05-16 15:35:01.0', date_to='3016-05-16 15:35:01.0', event=None,
                         number=0, offset=0, interval='hour'):
    global d
    date_from = datetime.strptime(date_from, '%Y-%m-%d %H:%M:%S.%f')
    date_to = datetime.strptime(date_to, '%Y-%m-%d %H:%M:%S.%f')
    events = []
    if event is not None:
        for elem in event:
            elem = re.compile(elem)
            events += [elem]
        to_find = {
            "Time": {"$gte": date_from, "$lte": date_to},
            "Event": {"$in": events}
        }
    else:
        to_find = {
            "Time": {"$gte": date_from, "$lte": date_to}
        }
    coll = get_collect(data_base)
    a = coll.find(to_find).sort("Time").skip(offset).limit(number)
    c = dumps(a, json_options=STRICT_JSON_OPTIONS)
    #print('c', c)

    to_group = {
        "year": {"$year": "$Time"},
        "month": {"$month": "$Time"},
        "day": {"$dayOfMonth": "$Time"},
        "hour": {"$hour": "$Time"},
    }
    to_sort = {
        "_id.hour": 1,
        "_id.day": 1,
        "_id.month": 1,
        "_id.year": 1,
    }
    if interval == 'day':
        del to_group["hour"]
        del to_sort["_id.hour"]
    if interval == 'month':
        del to_group["hour"]
        del to_group["day"]
        del to_sort["_id.hour"]
        del to_sort["_id.day"]
    if interval == 'year':
        del to_group["hour"]
        del to_group["day"]
        del to_group["month"]
        del to_sort["_id.hour"]
        del to_sort["_id.day"]
        del to_sort["_id.month"]
    b = []
    for elem in event:
        dict = {}
        dict["Event"] = elem
        to_find = {
            "Time": {"$gte": date_from, "$lte": date_to},
            "Event": re.compile(elem)
        }
        pipeline = [
            {"$match":to_find},
            {"$group": {"_id": to_group, "count": {"$sum": 1}}},
            {"$sort": to_sort}
        ]
        cursor = coll.aggregate(pipeline)
        dict["Result"] = list(cursor)
        b.append(dict)
    d = dumps(b)
 #   print('b', d)

    return {"a": c, "b": d}

def getLastDBUpdateDate(data_base = connection.local):
    if (data_base.update_date.count() != 0):
        last_date = data_base.update_date.find_one()
        return last_date['update_date']
    return 0

def saveLastDBUpdateDate(data_base = connection.local):
    coll = get_collect(data_base)
    size_db = len(list(coll.find()))
    last_date = coll.find()[size_db - 1].get("Time")
    current_date = last_date.strftime('%Y-%m-%d %H:%M:%S.%f')
    if (data_base.update_date.count() != 0):
        data_base.update_date.update({}, {"$set": {"update_date": current_date} })
        #data_base.update_date.find()
    else:
        data_base.update_date.insert({"update_date":current_date})

#pickup_from_database(date_from='1015-05-16 15:35:01.0', date_to='3016-05-16 15:35:01.0', event=['pdaemon'],interval='year')
