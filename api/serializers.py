import os

from rest_framework import serializers

from . import utils
from .models import Date


class DateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Date
        fields = ["id", "month", "day", "fact"]

    def create(self, validated_data):
        """
        Create and return a new "Date" instance.
        """
        validated_data["fact"] = utils.get_from_numbers_api(validated_data)
        month = validated_data["month"]
        if month.isnumeric():
            validated_data["month"] = utils.month_number_to_name(month)
        return Date.objects.create(**validated_data)

    def validate(self, data):
        if data["month"].isnumeric():
            month = int(data["month"])
        else:
            raise serializers.ValidationError({"message": "Month value is incorrect."})
        day = int(data["day"])
        if not (1 <= month <= 12):
            raise serializers.ValidationError({"message": "Month value is incorrect."})
        if not (1 <= day <= 31):
            raise serializers.ValidationError({"message": "Day value is incorrect."})
        try:
            date = Date.objects.get(
                month=utils.month_number_to_name(data["month"]), day=int(data["day"])
            )
            if date:
                fresh_fact = utils.get_from_numbers_api(data)
                if not date.fact == fresh_fact:
                    date.fact = fresh_fact
                date.popularity += 1
                date.save()
                raise serializers.ValidationError(
                    {"message": "This date already exists in db."}
                )
        except Date.DoesNotExist:
            pass
        return data


class DateDeleteSerializer(serializers.Serializer):
    pk = serializers.IntegerField()
    x_api_key = serializers.CharField()

    def validate(self, data):
        try:
            Date.objects.get(pk=data["pk"])
        except Date.DoesNotExist:
            raise serializers.ValidationError(
                {"message": "Invalid date id or date doesn't exist."}
            )
        if data["x_api_key"] == os.environ["SECRET_KEY"]:
            return data
        else:
            raise serializers.ValidationError({"message": "Wrong secret key."})

class PopularDateSerializer(serializers.Serializer):
    month = serializers.CharField()
    days_checked = serializers.CharField()
