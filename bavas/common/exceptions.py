from rest_framework.exceptions import APIException


class Bad_Request(APIException):
    status_code = 400
    default_detail = "Invalid excel uploaded"
    default_code = "invalid_excel"
