#from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import api.pimometer

class MyRESTView(APIView):

    def get(self, request, *args, **kw):
        """
        Get the details of a given event
        """

        event_id = request.GET.get('arg1', None)

        event_data = Pimometer.get_event_data(event_id)
        response = Response(event_data, status=status.HTTP_200_OK)

        return response
