from django_filters import rest_framework as filters
from v1.bills.models import *
from django.db.models import Q


class SearchFilter(filters.FilterSet):
    """filtering Entries"""
    search = filters.CharFilter(method='search_filter')
    date = filters.CharFilter(method='date_filter')

    class Meta:
        """Meta info"""
        model = Entries
        fields = "__all__"


    def search_filter(self, queryset, name, value):

        queryset = queryset.objects.filter(
            Q(vehicle__icontains=value) | Q(reg_no__icontains=value))

        return queryset


    def date_filter(self, queryset, name, value):
        """Returns queyset with in range of start date and end date"""

        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)

        queryset = queryset.objects.filter(
            date_field__range=(start_date, end_date))

        return queryset
