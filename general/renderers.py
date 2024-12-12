from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.utils.serializer_helpers import ReturnList, ReturnDict

class CustomJSONRenderer(JSONRenderer):
    """
    Custom JSON renderer to wrap the response in a consistence format.
    This renderer wrap the 2xx statuses inside "data" object,
    4xx statuses inside "errors" object,
    and 5xx status inside "message" object
    """
    def render(self, data, accepted_media_type=None, renderer_context=None):
        response = renderer_context.get('response', None)
        if response is not None:
            response_data = {
                'data': data
            }

            if response.status_code >= 400 and response.status_code < 500:
                response_data = {
                        'errors': data
                    }
            elif response.status_code >= 500:
                response_data = {
                    'message': "Internal Server Error"
                }
            elif response.status_code == status.HTTP_204_NO_CONTENT:
                response_data = {}

        return super(CustomJSONRenderer, self).render(response_data, accepted_media_type, renderer_context)