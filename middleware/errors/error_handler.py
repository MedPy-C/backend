import json
import logging

from django.http import HttpResponse


class Mediapp_beErrorMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):

        logging.exception(f'Error on {request}\n Error Message: {exception}')

        if not hasattr(exception, 'status_code'):
            return HttpResponse('Unexpected Error', status=500, content_type='application/json')

        status_code = exception.status_code
        message = exception.message
        error_code = exception.error_code

        response = {
            'error_code': error_code,
            'message': message
        }
        return HttpResponse(json.dumps(response), status=status_code, content_type='application/json')