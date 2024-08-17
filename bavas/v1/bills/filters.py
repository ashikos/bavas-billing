from django_filters import rest_framework as filters
from v1.bills.models import *
from django.db.models import Q
from django.db.models import F, Func, Value, CharField
from common import library as comm_lib


class EntryFilter(filters.FilterSet):
    """filtering Entries"""
    search = filters.CharFilter(method='search_filter')
    start_date = filters.CharFilter(method='date_filter')
    year = filters.CharFilter(method='year_filter')

    class Meta:
        """Meta info"""
        model = Entries
        fields = "__all__"

    def search_filter(self, queryset, name, value):

        value = value.replace(" ", "")

        queryset = queryset.annotate(reg=Func(
            F('reg_no'), Value(' '), Value(''), function='REPLACE',
            output_field=CharField()
        )).filter(
            Q(vehicle__icontains=value) | Q(reg__icontains=value)| Q(contact__icontains=value))
        return queryset

    def date_filter(self, queryset, name, value):
        """Returns queyset with in range of start date and end date"""
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)

        if start_date and not end_date:
            queryset = queryset.filter(date__gte=start_date)
        elif end_date and not start_date:
            queryset = queryset.filter(date__lte=end_date)
        else:
            queryset = queryset.filter(date__range=(start_date, end_date))
        return queryset

    def year_filter(self, queryset, name, value):
        """Returns queyset with in range of start date and end date"""
        if value:
            queryset = queryset.filter(date__year=value)

        return queryset


class BillFilter(filters.FilterSet):
    """filtering bill"""
    search = filters.CharFilter(method='search_filter')
    start_date = filters.CharFilter(method='date_filter')

    class Meta:
        """Meta info"""
        model = Bill
        fields = "__all__"

    def search_filter(self, queryset, name, value):

        value = value.replace(" ", "")

        queryset = queryset.annotate(reg=Func(
            F('reg_no'), Value(' '), Value(''), function='REPLACE',
            output_field=CharField()
        )).filter(
            Q(customer__icontains=value) | Q(reg__icontains=value))
        return queryset

    def date_filter(self, queryset, name, value):
        """Returns queyset with in range of start date and end date"""
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)

        if start_date and not end_date:
            queryset = queryset.filter(date__gte=start_date)
        elif end_date and not start_date:
            queryset = queryset.filter(date__lte=end_date)
        else:
            queryset = queryset.filter(date__range=(start_date, end_date))
        return queryset


class CustomerFilter(filters.FilterSet):
    """filtering bill"""
    search = filters.CharFilter(method='search_filter')

    class Meta:
        """Meta info"""
        model = Customer
        fields = "__all__"

    def search_filter(self, queryset, name, value):
        queryset = queryset.filter(
            Q(name__icontains=value) | Q(contact__icontains=value))
        return queryset
