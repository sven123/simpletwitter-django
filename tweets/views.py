from django_filters import rest_framework as filters
from rest_framework.decorators import action
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django.db.models import functions
from django.db.models import Count

import arrow
from arrow.parser import ParserError
from tweets import serializers
from tweets import models


class TweetFilter(filters.FilterSet):
    tag = filters.CharFilter(
        field_name="tag",
        label="tag",
        lookup_expr='iexact'
    )
    start = filters.CharFilter(label="start", method="filter_date")
    end = filters.CharFilter(label="end", method="filter_date")

    class Meta:
        model = models.Tweet
        fields = []

    def filter_date(self, queryset, name, value):
        try:
            dt = arrow.get(value, "YYYY-MM-DD")
        except ParserError as e:
            raise ValidationError({"start": str(e)})

        if name is "start":
            return queryset.filter(**{"created_at__gte": dt.datetime})
        else:
            return queryset.filter(
                **{"created_at__lte": dt.ceil('day').datetime}
            )


class TweetViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.TweetSerializer
    queryset = models.Tweet.objects.all()
    filter_class = TweetFilter

    @action(
        methods=["get"],
        detail=False,
        url_path="summary",
        url_name="Summary"
    )
    def summary(self, request, *args, **kwargs):
        frame = request.GET.get('timeframe', '').lower().strip()

        trunc_map = {
            'year': functions.TruncYear,
            '': functions.TruncYear,
            'month': functions.TruncMonth,
            'day': functions.TruncDay,
        }

        try:
            trunc_func = trunc_map[frame]
        except KeyError:
            raise ValidationError(
                {'timeframe': 'must be one of {}'.format(
                    [k for k in trunc_map.keys()]
                )}
            )

        qs = (
            self.filter_queryset(self.get_queryset())
            .annotate(time_frame=trunc_func('created_at'))
            .values('time_frame')
            .annotate(count=Count('*'))
            .order_by('time_frame')
        )

        sr = serializers.SummarySerializer(qs, many=True)
        return Response(sr.data)
