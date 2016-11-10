# Create your tests here.
import unittest

import pyparsing
from pymongo import MongoClient
from pyparsing import Word, alphas, nums, Suppress, OneOrMore, Group, ZeroOrMore


def parsing(input):
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
    # single_list[0] = datetime.strptime(single_list[0], '%Y-%m-%d %H:%M:%S.%f')
    return single_list


class TestWritingIntoDatabase(unittest.TestCase):
    def setUp(self):
        self.connection = MongoClient()
        self.db = self.connection.local
        self.collection = self.db.collect

    """ Записываем элемент в базу данных,а потом проверяем, стал ли размер базы данных равным 1"""

    def test_writing(self):
        entry = {"Time": "123", "UID": "1", "Event": "Test_Event"}
        self.collection.insert(entry)
        self.assertEqual(len(list(self.collection.find())), 1)

    def tearDown(self):
        self.db.collect.drop()


class TestPickupFromDatabase(unittest.TestCase):
    def setUp(self):
        self.connection = MongoClient()
        self.db = self.connection.local
        self.collection = self.db.collect
        entry = {"Time": "123", "UID": "1", "Event": "Test_Event"}
        entry_2 = {"Time": "123", "UID": "1", "Event": "werwr"}
        self.collection.insert(entry)
        self.collection.insert(entry_2)

    """ Тест по всевозможным ключам"""

    def tearDown(self):
        self.db.collect.drop()

    def test_pickup_from_database(self):
        self.true_case = self.collection.find({"Time": "123", "Event": "Test_Event"})
        self.false_case = self.collection.find({"Time": "321", "Event": "Test_Event"})
        self.true_case_2 = self.collection.find({"Time": "123"})
        self.assertEqual(len(list(self.true_case)), 1)
        self.assertEqual(len(list(self.false_case)), 0)
        self.assertEqual(len(list(self.true_case_2)), 2)


class TestParsing(unittest.TestCase):
    def setUp(self):
        self.test_string_true_1 = '[2016-05-13 16:07:01.155347460+03:00][18630]:pdaemon is already running.'
        self.test_string_true_2 = '[2016-05-13 16:16:19.454657576+03:00][18871]: /var/www/mooc-linux-programming/status/task exists: 9eb35974-c960-43e6-a8fe-1a8fc7d5a1bf'
        self.test_string_false = 'dsfdfs'
        self.test_true_result_1 = ['2016-05-13 16:07:01.155347', '18630', 'pdaemon is already running']
        self.test_true_result_2 = ['2016-05-13 16:16:19.454657', '18871',
                                   '/var/www/mooc-linux-programming/status/task exists: 9eb35974-c960-4']

    """ Тест на соответствие результатов парсинга правильным результатам"""

    def test_parsing(self):
        self.assertEqual(parsing(self.test_string_true_1), self.test_true_result_1)
        self.assertEqual(parsing(self.test_string_true_2), self.test_true_result_2)
        self.assertRaises(pyparsing.ParseException, parsing, self.test_string_false)


if __name__ == '__main__':
    unittest.main()
