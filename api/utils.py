import calendar

import requests

from .models import Date


def get_from_numbers_api(data):
    month = int(data["month"])
    day = int(data["day"])
    response = requests.get(f"http://numbersapi.com/{month}/{day}/date")
    return response.text


def month_number_to_name(month):
    return calendar.month_name[int(month)]


def get_popular_dates():
    dates = []
    query = Date.objects.filter(popularity__gt=0)
    for query_item in query:
        if not any(d["month"] == query_item.month for d in dates):
            month_dict = {"month": query_item.month, "days_checked": 1}
            dates.append(month_dict)
        else:
            dates_dict = next(
                (item for item in dates if item["month"] == query_item.month), None
            )
            dates_dict["days_checked"] += 1
    dates = sorted(dates, key=lambda x: x["days_checked"], reverse=True)
    return dates
