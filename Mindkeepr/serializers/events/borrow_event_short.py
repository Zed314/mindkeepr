from rest_framework import serializers

from Mindkeepr.models.events.borrow_event import BorrowEvent

class BorrowEventShortSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField(required=False)
    class Meta:
        model = BorrowEvent
        fields = ("id",)
        depth = 2