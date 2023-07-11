from rest_framework.serializers import HyperlinkedModelSerializer
from .models import Event


class EventSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Event
        fields = ('id', 'name', 'description', 'address', 'age_minimum', 'date', 'start_time', 'tickets_amount', 'type')


