from rest_framework import serializers
from tweets import models


class TweetSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Tweet
        fields = ('url', 'body', 'tag', 'created_at')
        extra_kwargs = {'created_at': {'read_only': True}}

    

class TimeFrameField(serializers.Field):
    def to_representation(self, value):
        return str(value.date())


class SummarySerializer(serializers.Serializer):
    count = serializers.IntegerField()
    time_frame = TimeFrameField()

