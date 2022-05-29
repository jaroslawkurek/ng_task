from django.contrib import admin
from .models import Date


@admin.register(Date)
class DateAdmin(admin.ModelAdmin):
    actions_on_top = True
    list_display = ("month", "day", "fact")
