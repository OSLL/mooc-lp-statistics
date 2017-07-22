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
    update_date = App.another_functions.getLastDBUpdateDate()
    return render(request, 'home.html', {'update_date': update_date})

def update_log_in_db(request):
    list_of_result_lists = App.another_functions.parsing()
    cnt_new_rows = len(list_of_result_lists)
    App.another_functions.writing_into_database(list_of_result_lists, App.another_functions.get_collect())

    App.another_functions.saveLastDBUpdateDate()
    update_date = App.another_functions.getLastDBUpdateDate()
    return render(request, 'update_log_in_db.html', {'count_new_rows':cnt_new_rows, 'update_date': update_date})


def get(request):
    date_from = request.GET['date_from']
    date_to = request.GET['date_to']
    event = QueryDict(request.get_full_path())
    event = event.getlist('event')
    interval = request.GET['selected_interval']

    results = App.another_functions.parsing()
    App.another_functions.writing_into_database(results, App.another_functions.get_collect())
    Col = App.another_functions.dumps(App.another_functions.pickup_from_database(event= event, date_from= date_from, date_to= date_to, interval = interval))

    return render(request, 'list_view.html', {'collection': Col})

def get_log_entry(request):
    log_id = request.GET['id']
    record_set = App.another_functions.getLogRecordSet(log_id)
    #return render(request, 'get_log_entry.html', {'record_set' : record_set})
    return HttpResponse(record_set)