from rest_framework import serializers

from App.models import Update


class UpdateSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Update
        fields = ('date_from', 'date_to', 'event')
