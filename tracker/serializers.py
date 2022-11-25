from rest_framework import serializers

from tracker.models import Tracker


class TrackerSerializer(serializers.ModelSerializer):
    at_tracking = serializers.ReadOnlyField()
    matched = serializers.ReadOnlyField()
    matched_date = serializers.ReadOnlyField()

    class Meta:
        model = Tracker
        exclude = ["investors", "last_updated"]

