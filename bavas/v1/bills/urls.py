from rest_framework.routers import SimpleRouter

from django.urls import path
from v1.bills import views
from v1.bills.models import *

router = SimpleRouter()

router.register(r'bill', views.BillView, basename=Bill)
router.register(r'service', views.ServiceView, basename=Service)
router.register(r'entry', views.EntriesView, basename=Entries)
router.register(r'customer', views.CustomerView, basename=Customer)

urlpatterns = [
    path('billtopdf/<int:id>/', views.PDFView.as_view(), name='pdf'),
    path('excel/', views.ExcelView.as_view()),
    path('perfomance/', views.WashPerfomanceView.as_view()),
]

urlpatterns += router.urls
