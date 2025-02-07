from django.urls import path
from .views import download_psql_dump_view

urlpatterns = [
    path('download-db/', download_psql_dump_view, name='download_psql_dump'),
]
