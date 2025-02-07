import os
from django.http import FileResponse, HttpResponse
from v1.accounts import utils


def download_psql_dump_view(request):
    """
    Django view to download a PostgreSQL database dump file.
    """
    try:
        dump_file = utils.get_psql_dump_file()
        response = FileResponse(open(dump_file, 'rb'), as_attachment=True)
        response['Content-Disposition'] = f'attachment; filename="{os.path.basename(dump_file)}"'
        return response
    except Exception as e:
        return HttpResponse(f"Error: {str(e)}", status=500)