from django.forms import widgets
from rest_framework import serializers
from api.models import Api

class ApiSerializer(serializers.Serializer):
    title = serializers.CharField(required=True)
    s1 = serializers.CharField()
