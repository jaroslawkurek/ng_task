import calendar

import requests

from .models import Date
from django.db.models import Count


def get_from_numbers_api(data):
    month = int(data["month"])
    day = int(data["day"])
    response = requests.get(f"http://numbersapi.com/{month}/{day}/date")
    return response.text


def month_number_to_name(month):
    return calendar.month_name[int(month)]


def get_popular_dates():
    return (
        Date.objects.values("month")
        .annotate(days_checked=Count("day"))
        .order_by("-days_checked")
    )
