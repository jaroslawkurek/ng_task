from django.contrib import admin
from django.urls import path
from api import views
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("dates/", views.DateApiView.as_view(), name="dates"),
    path("popular/", views.PopularApiView.as_view(), name="dates"),
    path("dates/<int:pk>/", views.DateApiDelete.as_view(), name="dates_delete"),
    path("__debug__/", include("debug_toolbar.urls")),
]
