from django.http import HttpResponse
from django.http import QueryDict
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer

import App.another_functions
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
    list_of_result_lists = App.another_functions.parsing()
    App.another_functions.writing_into_database(list_of_result_lists, App.another_functions.get_collect())
    return render(request, 'home.html')


def get(request):
    date_from = request.GET['date_from']
    date_to = request.GET['date_to']
    event = QueryDict(request.get_full_path())
    event = event.getlist('event')

    results = App.another_functions.parsing()
    App.another_functions.writing_into_database(results, App.another_functions.get_collect())
    Col = App.another_functions.dumps(App.another_functions.pickup_from_database(event= event, date_from= date_from, date_to= date_to, interval ='day'))

    return render(request, 'list_view.html', {'collection': Col})