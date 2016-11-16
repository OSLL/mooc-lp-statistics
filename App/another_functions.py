import codecs
from datetime import datetime

from pymongo import MongoClient
from pyparsing import Word, alphas, nums, Suppress, OneOrMore, Group, ZeroOrMore


def parsing():
    list_of_result_lists = []
    file = codecs.open("App/static/txt/test_log", "r", "utf_8_sig")

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
        print(single_list)
        return single_list

    # Построчный парсинг
    for line in file:
        if not line.startswith('['):
            continue
        list_of_result_lists += [razbor_stroki(line)]
    return list_of_result_lists


def pickup_from_database(collection, date_from, date_to, event):
    date_from = datetime.strptime(date_from, '%Y-%m-%d %H:%M:%S.%f')
    date_to = datetime.strptime(date_to, '%Y-%m-%d %H:%M:%S.%f')
    a = collection.find({"Time": {"$gte": date_from, "$lte": date_to}, "Event": event}).sort("Time")
    return a


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