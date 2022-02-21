from rest_framework import status
from rest_framework.response import Response


def custom_exception_handler(exc, context):
    _status = status.HTTP_200_OK

    message = exc.detail.__str__() if hasattr(exc, 'detail') else exc.__str__()

    data = {'msg': message}

    return Response(data=data, status=_status)
