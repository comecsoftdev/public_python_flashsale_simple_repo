from rest_framework import status
from rest_framework.response import Response


def custom_exception_handler(exc, context):
    _status = status.HTTP_404_NOT_FOUND

    message = exc.detail.__str__() if hasattr(exc, 'detail') else exc.__str__()
    _status = exc.result_code if hasattr(exc, 'result_code') else getattr(exc, 'status_code', _status)

    data = {'msg': message}

    return Response(data=data, status=_status)
