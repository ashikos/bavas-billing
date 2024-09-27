
import pandas as pd
from v1.bills import models as bill_models
from django.db.models import Q

def Generate_bill_pdf(request, sponsors):
    """Function to Generate Sponsor logos pdf"""

    elements = []

    return elements


def Check_amount_type(df, row):
    """Function to Generate Sponsor logos pdf"""

    amount, gpay, is_credit_received = None, None, False
    if not pd.isna(df.iloc[row, 6]):
        amount = None if pd.isna(df.iloc[row, 6]) else df.iloc[row, 6]
    if not pd.isna(df.iloc[row, 7]):
        gpay = None if pd.isna(df.iloc[row, 7]) else df.iloc[row, 7]

    if not pd.isna(df.iloc[row, 10]):
        amount = None if pd.isna(df.iloc[row, 10]) else df.iloc[row, 10]
        is_credit_received = True
    if not pd.isna(df.iloc[row, 11]):
        gpay = None if pd.isna(df.iloc[row, 11]) else df.iloc[row, 11]
        is_credit_received = True

    return amount, gpay, is_credit_received


def get_collection_date(year):
    """Function to get statics of Entries """

    full = bill_models.Entries.objects.filter(
        date__year=year, type__istartswith="f").count()
    body = bill_models.Entries.objects.filter(
        date__year=year, type__istartswith="b").count()
    quick = bill_models.Entries.objects.filter(
        date__year=year, type__istartswith="Q").count()
    wash = bill_models.Entries.objects.filter(
        date__year=year, type__istartswith="w").count()
    paint = bill_models.Entries.objects.filter(date__year=year).filter(
        Q(type__icontains='coat') | Q(type__icontains='paint')
    ).count()
    exclude_list = ['F', 'B', 'Q', 'U', 'W']
    others = bill_models.Entries.objects.filter(date__year=year).filter(
        ~Q(type__istartswith="f") & ~Q(type__istartswith="b")
        & ~Q(type__istartswith="q") & ~Q(type__istartswith="w")
        & ~Q(type__istartswith="u")
    ).count()

    # for i in others:
    #     print(i.type)

    data = {
        "full": full,
        "body": body,
        "quick": quick,
        "wash": wash,
        "paint": paint,
        "others": others
    }
    return data


def get_entry_graph_data(year=None):

    if not year:
        query_set = bill_models.Entries.objects.all()
    else:
        query_set = bill_models.Entries.objects.filter(date__year=year)

    coordinates = []
    for i in range(1, 13):
        entry_count = query_set.filter(date__month=i).count()
        coordinates.append(entry_count)
    return coordinates












