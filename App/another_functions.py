# -*- coding: utf-8 -*-
import codecs
from datetime import datetime

from pymongo import MongoClient
from pyparsing import Word, alphas, nums, Suppress, OneOrMore, Group, ZeroOrMore
from bson.json_util import dumps, STRICT_JSON_OPTIONS
import os

def parsing():
    list_of_result_lists = []
    # HACK - replace hardcode with taking path from settings
    # https://github.com/OSLL/mooc-lp-statistics/issues/44  
    base_dir = os.path.dirname(os.path.abspath(__file__))
    logpath = os.path.join(base_dir, 'static/txt/test_log')
    logfile = codecs.open(logpath, "r", "utf_8_sig")
 #   logfile = codecs.open("/var/www/mooc-lp-statistics/App/static/txt/test_log", "r", "utf_8_sig")
    # do not use file as a variable name (it is a module name)

    def razbor_stroki(input):
        list_of_result_lists = []
        # Правило для парсинга даты
        parse_time = Suppress("[") + Word("[" + "-" + nums) + Word(nums + ":" + "." + "+") + Suppress("]")
        # Правило для парсинга уникалного номера
        parse_number = Suppress("[") + Word(nums) + Suppress("]") + Suppress(Word(":"))
        # Правило для парсинга события, состояещего только из слов( например,pdaemon is already running)
        parse_only_alphas_event = OneOrMore(Word(alphas))
        # Правило для парсинга события,состоящего из всякого(
        # например, /var/www/mooc-linux-programming/status/task exists: 9eb35974-c960-43e6-a8fe-1a8fc7d5a1bf)
        parse_mooc_event = Word("/" + alphas + "-" + ":") + Word(alphas + ":") + Word(alphas + nums + "-")
        # Правило для парсинга событий лога любого типа
        parse_event = ZeroOrMore(parse_only_alphas_event) + ZeroOrMore(parse_mooc_event)
        # Открытие лог-файла в кодировке UTF-8
        # Конечное правило для парсинга строк. Составляюие даты сгруппируются в 1 список,
        # уникальный номер во второй список,событие в третий список
        parse_module = Group(parse_time) + Group(parse_number) + Group(parse_event)
        # Результат парсинга(
        parse_result = parse_module.parseString(input)
        # Список, содержащий результаты разбора одной строки
        single_list = []
        """
        Описание цикла:
        Для каждого элемента,кроме последнего, каждого списка
        добавить пробел(при парсинге он теряется).
        Затем элементы каждого отдельного списка собираются в отдельную строку.
        Затем каждая строка(всего их 3 добавляется в список).
        Итог:
            Входные данные:строка,которую нам нужно разобрать
            ( например,[2016-05-14 17:25:01.642065713+03:00][4281]:pdaemon is already running.)
            Выходные данные: Список,состоящий из 3-х строк-элементов
        """
        for elem in parse_result:
            elem[len(elem) - 1] = elem[len(elem) - 1][:15]
        for elem in parse_result:
            for i in range(len(elem) - 1):
                elem[i] += " "
            complete_string = ''
            for x in elem:
                complete_string += x
            single_list.append(complete_string)
        single_list[0] = datetime.strptime(single_list[0], '%Y-%m-%d %H:%M:%S.%f')
        return single_list

    # Построчный парсинг
    for line in logfile:
        if not line.startswith('['):
            continue
        list_of_result_lists += [razbor_stroki(line)]
    return list_of_result_lists


def pickup_from_database(date_from='1015-05-16 15:35:01.0', date_to='3016-05-16 15:35:01.0', event=None,
                         number=0, offset=0, interval=None):

    global d
    c = None
    date_from = datetime.strptime(date_from, '%Y-%m-%d %H:%M:%S.%f')
    date_to = datetime.strptime(date_to, '%Y-%m-%d %H:%M:%S.%f')
    a = db.collect.find({"Time": {"$gte": date_from, "$lte": date_to}, "Event": event}).sort("Time").skip(offset).limit(
        number)
    c = dumps(a ,json_options= STRICT_JSON_OPTIONS)
    length = len(list(c))
    print(length)
    if length > 2:
        if interval == 'hour' :
            b = db.collect.aggregate(
                [
                    {
                        "$match": {
                            "Time": {"$gte": date_from, "$lte": date_to}
                        }
                    },
                    {
                        "$group": {
                            "_id": {"year": {"$year": "$Time"},"month": {"$month": "$Time"}, "day": {"$dayOfMonth": "$Time"}, "hour": {"$hour": "$Time"}},
                            "count": {"$sum": 1}
                        }
                    },
                    {
                        "$sort" : {
                            "_id.hour": 1,
                            "_id.day": 1,
                            "_id.month": 1,
                            "_id.year": 1,

                        }
                    },
                ]
                )
            d = dumps(b)
            for_draw =[]
            for elem in b:
                single_stat = (str(elem['_id']['hour']) + '.' + str(elem['_id']['day']) + '.' + str(elem['_id']['month']) + '.' + str(elem['_id']['year']), str(elem['count']))
                for_draw += [single_stat]


        elif interval == 'day':
            b = db.collect.aggregate(
                [
                    {
                        "$match": {
                            "Time": {"$gte": date_from, "$lte": date_to}
                        }
                    },
                    {
                        "$group": {
                            "_id": {"year": {"$year": "$Time"},"month": {"$month": "$Time"}, "day": {"$dayOfMonth": "$Time"}},
                            "count": {"$sum": 1}
                        }
                    },
                    {
                        "$sort" : {
                            "_id.day": 1,
                            "_id.month": 1,
                            "_id.year": 1,

                        }
                    },

                ]
                )
            d = dumps(b)
            for_draw = []
            for elem in b:
                single_stat = (
                str(elem['_id']['day']) + '.' + str(elem['_id']['month']) + '.' + str(
                    elem['_id']['year']), str(elem['count']))
                for_draw += [single_stat]


        elif interval == 'month':
            b = db.collect.aggregate(
                [
                    {
                        "$match": {
                            "Time": {"$gte": date_from, "$lte": date_to}
                        }
                    },
                    {
                        "$group": {
                            "_id": {"year": {"$year": "$Time"},"month": {"$month": "$Time"}},
                            "count": {"$sum": 1}
                        }
                    },
                    {
                        "$sort" : {
                            "_id.month": 1,
                            "_id.year": 1,

                        }
                    },
                ]
                )
            d = dumps(b)
            for_draw = []
            for elem in b:
                single_stat = (
                str(elem['_id']['month']) + '.' + str(
                    elem['_id']['year']), str(elem['count']))
                for_draw += [single_stat]

    return { "a" : c, "b" : d}


def writing_into_database(results, coll):
    length = len(list(collection.find()))
    if length != 0:
        for elem in results:
            if elem[0] > results[length - 1][0]:
                entry = {"Time": elem[0], "UID": elem[1], "Event": elem[2]}
                coll.insert(entry)
    else:
        for elem in results:
            entry = {"Time": elem[0], "UID": elem[1], "Event": elem[2]}
            coll.insert(entry)


connection = MongoClient()

db = connection.local
collection = db.collect
db.collect.create_index("Event")
db.collect.create_index("Time")
