from django.urls import path
from .views import *

urlpatterns = [
    path('download-db/', download_psql_dump_view, name='download_psql_dump'),
    path('login/', verify_login, name='verify_login'),
]
