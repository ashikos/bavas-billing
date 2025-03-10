import os
from django.http import FileResponse, HttpResponse
from v1.accounts import utils
from django.http import JsonResponse
from v1.accounts import serializer as auth_serializer
from rest_framework.decorators import api_view
from v1.accounts import models as acc_models
from rest_framework import status


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


def authenticate_user(username, raw_password):
    """
        Function to authenticate user with username and raw password
        returns user if user exists with username and password
        else returns None
    """
    try:
        user = acc_models.UserMaster.objects.get(username=username)
        if user.check_password(raw_password):
            return user
    except :
        return False


@api_view(['POST'])
def verify_login(request):
    """
    Method for checking login type
    """
    serializer = auth_serializer.LoginSerializer(data=request.data)
    if serializer.is_valid():
        try:
            username = request.data['username']
            password = request.data['password']

            user = authenticate_user(username=username, raw_password=password)
            print(user)

            token = user.create_access_token
            result = {
                'AccessKey': str(token),
                'UsrId': user.id,
                'username': user.username,
                'user_type': user.user_type,
            }
            final_data = result
        except Exception as e:
            print(e)
            final_data = {"detail": str(e)}
    else:
        final_data = {}

    return JsonResponse(final_data, status=status.HTTP_200_OK)

