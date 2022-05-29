from email import header
import pytest
from api.models import Date
from rest_framework.test import APIClient
import os


@pytest.fixture()
def dates_url(live_server):
    url = live_server.url + "/dates/"
    return url


# Added here pk from an existing date fixture.
@pytest.fixture()
def dates_with_date_id_url(live_server, date_fixture):
    url = live_server.url + "/dates/{date_id}/".format(date_id=int(date_fixture.pk))
    return url


@pytest.fixture()
def dates_with_date_wrong_id_url(live_server):
    url = live_server.url + "/dates/2077/"
    return url


@pytest.fixture()
def popular_url(live_server):
    url = live_server.url + "/popular/"
    return url


@pytest.fixture
def date_fixture():
    date = Date.objects.create(
        month="April", day=22, fact="i'm_a_fixture", popularity=2
    )
    return date


@pytest.fixture
def date_fixture_2():
    date = Date.objects.create(
        month="April", day=20, fact="i'm_also_a_fixture", popularity=2
    )
    return date


# POST
def test_create_date_success(dates_url):
    data = {"month": 4, "day": 1}
    response = APIClient().post(dates_url, data)
    date = Date.objects.get(month="April", day=1)
    assert not date.fact == ""  # "" is the default value
    assert response.status_code == 201


def test_create_date_month_out_of_scope(dates_url):
    data = {"month": 13, "day": 1}
    response = APIClient().post(dates_url, data)
    assert response.json() == {"message": ["Month value is incorrect."]}
    assert response.status_code == 400


def test_create_date_day_out_of_scope(dates_url):
    data = {"month": 4, "day": 32}
    response = APIClient().post(dates_url, data)
    assert response.json() == {"message": ["Day value is incorrect."]}
    assert response.status_code == 400


def test_create_date_with_month_as_name(dates_url):
    data = {"month": "April", "day": 1}
    response = APIClient().post(dates_url, data)
    assert response.json() == {"message": ["Month value is incorrect."]}
    assert response.status_code == 400


def test_create_date_that_already_exists(dates_url, date_fixture):
    data = {"month": 4, "day": 22}
    response = APIClient().post(dates_url, data)
    date = Date.objects.get(month="April", day=22)
    assert not date.fact == date_fixture.fact
    assert response.json() == {"message": ["This date already exists in db."]}
    assert response.status_code == 400


# GET
def test_get_dates(dates_url, date_fixture, date_fixture_2):
    response = APIClient().get(dates_url)
    for data in response.json():
        assert data["month"] == "April"
    assert response.status_code == 200


def test_get_popular(popular_url, date_fixture, date_fixture_2):
    response = APIClient().get(popular_url)
    for data in response.json():
        assert not data["days_checked"] == 0
    assert response.status_code == 200


# DELETE
def test_delete_date_success(dates_with_date_id_url, date_fixture):
    response = APIClient().delete(
        dates_with_date_id_url, HTTP_X_API_KEY=os.environ["SECRET_KEY"]
    )
    date = Date.objects.filter(pk=date_fixture.pk)
    assert response.status_code == 204
    assert not date.exists()


def test_delete_date_wrong_secret_key(dates_with_date_id_url, date_fixture):
    response = APIClient().delete(
        dates_with_date_id_url, HTTP_X_API_KEY="failure_test_secret_key"
    )
    assert response.status_code == 400
    assert response.json() == {"message": ["Wrong secret key."]}


def test_delete_date_which_doesnt_exist(dates_with_date_wrong_id_url):
    response = APIClient().delete(
        dates_with_date_wrong_id_url, HTTP_X_API_KEY=os.environ["SECRET_KEY"]
    )
    assert response.status_code == 400
    assert response.json() == {"message": ["Invalid date id or date doesn't exist."]}
