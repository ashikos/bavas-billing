from django_filters import rest_framework as filters
from v1.bills.models import *
from django.db.models import Q
from django.db.models import F, Func, Value, CharField
from common import library as comm_lib


class EntryFilter(filters.FilterSet):
    """filtering Entries"""
    search = filters.CharFilter(method='search_filter')
    start_date = filters.CharFilter(method='date_filter')

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
            Q(vehicle__icontains=value) | Q(reg__icontains=value))
        return queryset

    def date_filter(self, queryset, name, value):
        """Returns queyset with in range of start date and end date"""
        print(23434343)
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)

        print(start_date, end_date)
        # start_date = comm_lib.convert_str_to_datetime(start_date, '%d/%m/%Y')
        # end_date = comm_lib.convert_str_to_datetime(end_date, '%d/%m/%Y')
        queryset = queryset.filter(date__range=(start_date, end_date))

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

        # start_date = comm_lib.convert_str_to_datetime(start_date, '%d/%m/%Y')
        # end_date = comm_lib.convert_str_to_datetime(end_date, '%d/%m/%Y')
        queryset = queryset.filter(date__range=(start_date, end_date))

        return queryset


class CustomerFilter(filters.FilterSet):
    """filtering bill"""
    search = filters.CharFilter(method='search_filter')

    class Meta:
        """Meta info"""
        model = Bill
        fields = "__all__"

    def search_filter(self, queryset, name, value):

        queryset = queryset.filter(Q(name=value) | Q(contact=value))
        return queryset
