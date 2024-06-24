from django.http import JsonResponse
from django.views import View

class Custom500ErrorView(View):
    def dispatch(self, request, *args, **kwargs):
        response_data = {
            'message': 'Internal server error'
        }
        return JsonResponse(response_data, status=500)