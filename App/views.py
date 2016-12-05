from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer

from App.another_functions import *
from App.models import Find_in_database
from App.serializers import Find_in_databaseSerializer


class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """

    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


@csrf_exempt
def Find_in_database_list(request):
    if request.method == 'GET':
        snippets = Find_in_database.objects.all()
        serializer = Find_in_databaseSerializer(snippets, many=True)
        return JSONResponse(serializer.data)


def home(request):
    list_of_result_lists = parsing()
    writing_into_database(list_of_result_lists, collection)
    return render(request, 'home.html')


def get(request):
    try:
        date_from = request.GET['date_from']
    except:
        date_from = None
    try:
        date_to = request.GET['date_to']
    except:
        date_to = None
    try:
        event = request.GET['event']
    except:
        event = None

    Col = pickup_from_database(event= event, date_from= date_from, date_to= date_to, interval = 'hour')
    list = Col['a']
    stat = Col['b']
    print(list)
    print(stat)
    return render(request, 'list_view.html', {'list': list}, {'stat': stat})
