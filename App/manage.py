from App.models import Find_in_database
from App.serializers import Find_in_databaseSerializer
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from django.utils.six import BytesIO

find_in_database = Find_in_database(date_from='21.10.2016', date_to='22.10.2016')
find_in_database.save()


serializer = Find_in_databaseSerializer(find_in_database)
content = JSONRenderer().render(serializer.data)


stream = BytesIO(content)
data = JSONParser().parse(stream)