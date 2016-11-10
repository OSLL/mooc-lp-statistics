import codecs
from datetime import datetime

from django.http import Http404
from django.shortcuts import render
from pymongo import MongoClient
from pyparsing import Word, alphas, nums, Suppress, OneOrMore, Group, ZeroOrMore
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from App.models import Find_in_database
from App.serializers import Find_in_databaseSerializer


class Find_in_databaseList(APIView):
    """
    List all Find_in_databases, or create a new Find_in_database.
    """

    def get(self, request, format=None):
        Find_in_databases = Find_in_database.objects.all()
        serializer = Find_in_databaseSerializer(Find_in_databases, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = Find_in_databaseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Find_in_databaseDetail(APIView):
    """
    Retrieve, update or delete a Find_in_database instance.
    """

    def get_object(self, pk):
        try:
            return Find_in_database.objects.get(pk=pk)
        except Find_in_database.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        Find_in_database = self.get_object(pk)
        serializer = Find_in_databaseSerializer(Find_in_database)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        Find_in_database = self.get_object(pk)
        serializer = Find_in_databaseSerializer(Find_in_database, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        Find_in_database = self.get_object(pk)
        Find_in_database.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


connection = MongoClient()
db = connection.local
collection = db.collect


def pickup_from_database(collection, date_from, date_to, event):
    date_from = datetime.strptime(date_from, '%Y-%m-%d %H:%M:%S.%f')
    date_to = datetime.strptime(date_to, '%Y-%m-%d %H:%M:%S.%f')
    a = collection.find({"Time": {"$gte": date_from, "$lte": date_to}, "Event": event}).sort("Time")
    return a


def writing_into_database(results, coll):
    for elem in results:
        entry = {"Time": elem[0], "UID": elem[1], "Event": elem[2]}
        coll.insert(entry)


def home(request):
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
    file = codecs.open("App/static/txt/test_log", "r", "utf_8_sig")

    # Функция для парсинга
    def parsing(input):
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
        print(single_list)
        return single_list

    # Построчный парсинг
    for line in file:
        if not line.startswith('['):
            continue
        list_of_result_lists += [parsing(line)]
    #writing_into_database(list_of_result_lists, collection)
    Col = pickup_from_database(collection, '2016-05-13 15:33:01.0', '2016-05-16 15:35:01.0',
                               "pdaemon is already running")
    return render(request, 'home.html', {'collection': Col})
