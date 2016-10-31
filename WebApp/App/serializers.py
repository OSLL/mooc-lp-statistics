from django.contrib.auth.models import User, Group, Permission
from rest_framework import serializers
from WebApp.App.models import Update


class UpDateSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Update
        fields = ('lod_name',
                  'log_update')


