from django.http import Http404
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

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
    print(len(list(collection.find())))
    Col = pickup_from_database(collection, '2016-05-13 15:33:01.0', '2016-05-16 15:35:01.0',
                               "pdaemon is already running")
    return render(request, 'home.html', {'collection': Col})
