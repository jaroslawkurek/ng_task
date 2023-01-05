from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from . import utils
from .models import Date
from .serializers import DateDeleteSerializer, DateSerializer, PopularDateSerializer


class DateApiView(APIView):
    """
    Retrieve, Create
    """

    def get(self, request, format=None):
        dates = Date.objects.all()
        serializer = DateSerializer(dates, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = DateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class DateApiDelete(APIView):
    """
    Delete
    """

    def delete(self, request, pk, format=None):
        data = {"pk": pk, "x_api_key": request.META["HTTP_X_API_KEY"]}
        serializer = DateDeleteSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        date = Date.objects.get(pk=pk)
        date.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PopularApiView(APIView):
    """
    Retrieve Popular Days
    """

    def get(self, format=None):
        dates = utils.get_popular_dates()
        serializer = PopularDateSerializer(dates, many=True)
        return Response(serializer.data)
