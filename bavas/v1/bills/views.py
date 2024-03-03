import  openpyxl
import pandas as pd

from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response

from datetime import datetime

from v1.bills import models as bill_models
from v1.bills import serializers as bill_serializers

from v1.bills.utils import Generate_bill_pdf
from v1.bills.utils import Check_amount_type

# from v1.accounts import permissions
# Create your views here.


class BillView(viewsets.ModelViewSet):
    """views for vendors"""

    queryset = bill_models.Bill.objects.all()
    serializer_class = bill_serializers.BillSerializer


class ServiceView(viewsets.ModelViewSet):
    """views for vendors"""

    queryset = bill_models.Service.objects.all()
    serializer_class = bill_serializers.ServiceSerializer


class EntriesView(viewsets.ModelViewSet):
    """views for vendors"""

    queryset = bill_models.Entries.objects.all()
    serializer_class = bill_serializers.EntriesSerializer
    # filterset_class = group_filter.GroupFilter


class PDFView(APIView):
    """View for generating pdf bill"""

    def get(self, request, *args, **kwargs):

        bill_id = 1
        bill = bill_models.Bill.objects.get(id=bill_id)
        items = bill.items.all()


        # return generate_bill_pdf


class ExcelView(APIView):
    """View to update the entries using excel
     Attribs:
        excel(file): excel file report
        date(str): %d-%m-%Y format
    """

    http_method_names = ['post']

    def post(self, *args, **kwargs):

        data = self.request.data
        excel_file = data['excel']
        date = data['date']
        date_object = datetime.strptime(date, "%d-%m-%Y").date()
        sheet_name = str(date_object.day)


        df = pd.read_excel(excel_file, sheet_name=sheet_name)
        df = df.where(pd.notnull(df), None)

        for row in range(1, 50):
            data = {
                "reg_no": df.iloc[row, 1] if not pd.isna(
                    df.iloc[row, 1]) else None,
                "mob": df.iloc[row, 2] if not pd.isna(
                    df.iloc[row, 2]) else None,
                "vehicle": df.iloc[row, 3] if not pd.isna(
                    df.iloc[row, 3]) else None,
                "service_type": df.iloc[row, 4] if not pd.isna(
                    df.iloc[row, 4]) else None,
            }
            if any(value and not str(value).isspace() for value in data.values()):
                print("element is : ", data)

                entry, created = bill_models.Entries.objects.get_or_create(
                    reg_no=data['reg_no'], date=date_object, contact=data['mob'])

                entry.contact = data['mob']
                entry.vehicle = data['vehicle']
                entry.type = data['service_type']

                amount, gpay, is_credit_received = Check_amount_type(df, row)
                entry.amount = amount
                entry.gpay = gpay
                entry.is_credit_received = is_credit_received
                entry.date = date_object

                entry.save()
                ids = entry.id
                ent = bill_models.Entries.objects.get(id=ids)
                print(ent.vehicle, ent.id)




        return Response({"response": "all set"})
