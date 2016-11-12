from django.http import Http404
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from App.another_functions import *
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




def home(request):
    list_of_result_lists = parsing()
    writing_into_database(list_of_result_lists, collection)
    print(len(list(collection.find())))
    Col = pickup_from_database(collection, '2016-05-13 15:33:01.0', '2016-05-16 15:35:01.0',
                               "pdaemon is already running")
    return render(request, 'home.html', {'collection': Col})
