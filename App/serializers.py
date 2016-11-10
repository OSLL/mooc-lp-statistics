from rest_framework import serializers

from App.models import Find_in_database


class Find_in_databaseSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Find_in_database
        fields = ('date_from', 'date_to', 'event')
