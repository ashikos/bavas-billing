import pandas as pd
from django.http import HttpResponse
import os

from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response

from datetime import datetime

from v1.bills import models as bill_models
from v1.bills import serializers as bill_serializers
from v1.bills import utils
from common.exceptions import Bad_Request
from v1.bills.constants import MONTH_ATTRS
from v1.bills.task import test_func
from v1.bills.utils import generate_pdf

from v1.bills.utils import Check_amount_type

from v1.bills import filters as bill_filters

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')


class BillView(viewsets.ModelViewSet):
    """views for vendors"""

    queryset = bill_models.Bill.objects.all().order_by("-date", "id")
    serializer_class = bill_serializers.BillSerializer
    filterset_class = bill_filters.BillFilter


class CustomerView(viewsets.ModelViewSet):
    """views for vendors"""

    queryset = bill_models.Customer.objects.all().order_by("-id")
    serializer_class = bill_serializers.CustomerSerializer
    filterset_class = bill_filters.CustomerFilter


class EntriesView(viewsets.ModelViewSet):
    """views for vendors"""

    queryset = bill_models.Entries.objects.all().order_by("-date", "id")
    serializer_class = bill_serializers.EntriesSerializer
    filterset_class = bill_filters.EntryFilter


class PDFView(APIView):
    """View for generating pdf bill"""

    def get(self, request, *args, **kwargs):
        bill_id = kwargs['id']
        bill = bill_models.Bill.objects.get(id=bill_id)
        items = bill.items.all()

        serializer = bill_serializers.BillSerializer(bill)

        template = TEMPLATES_DIR + '/temp.html'

        con_data = {
            "bill": serializer.data,
            "items": items
        }
        context = {"data": con_data}

        response = generate_pdf( template, context)

        return response


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
        year, month = date.split('-')

        for day in range(1, MONTH_ATTRS[month][0]):
            date = f"{year}-{month}-{day}"
            print(date)
            try:
                date_object = datetime.strptime(date, "%Y-%m-%d").date()
                sheet_name = str(date_object.day)


                df = pd.read_excel(excel_file, sheet_name=sheet_name)
                df = df.where(pd.notnull(df), None)

                for row in range(1, 50):
                    print("row:" , row)

                    if pd.isna(df.iloc[row, 0]):
                        break

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
                    if any(value and not str(value).isspace() for value in
                           data.values()):
                        entry, created = bill_models.Entries.objects.get_or_create(
                            reg_no=data['reg_no'], date=date_object,
                            contact=data['mob'])

                        entry.vehicle = data['vehicle']
                        entry.type = data['service_type']

                        amount, gpay, is_credit_received = Check_amount_type(
                            df, row)
                        entry.amount = amount
                        entry.gpay = gpay
                        entry.is_credit_received = is_credit_received
                        entry.date = date_object

                        entry.save()
                        ids = entry.id
                        ent = bill_models.Entries.objects.get(id=ids)
            except:
                raise Bad_Request(f"Invalid excel uploded, Error on day:{day} row: {row}")

        return Response("excel uploaded succesfully")


class WashPerfomanceView(APIView):

    def get(self, request, *args, **kwargs):
        year = self.request.query_params.get('year', None)

        type_wise = utils.get_collection_date(year)
        monthly = utils.get_entry_graph_data(year)
        data = {
            "type_wise": type_wise,
            "monthly": monthly,
        }

        return Response({"response": data})


# class LoginView(APIView):
#
#     def post(self, request):
#         username = request.data['username']
#         password = request.data['password']
#
#         if not username == 'ashik.os@cide.in':
#             raise AuthenticationFailed("Username Incorrect")
#         elif not password == '1234':
#             raise AuthenticationFailed("password incorrectt")
#         else:
#             message = "Successfully logged"
#
#         response = Response()
#
#         response.data = {
#             "message": message
#         }
#
#         return response


def TestView(request):
    test_func.delay()
    return HttpResponse("Donnneee")

