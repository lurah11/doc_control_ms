
import threading

_thread_local = threading.local()

class RequestMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Set request in thread-local storage
        _thread_local.request = request
        response = self.get_response(request)
        return response

    @staticmethod
    def get_request():
        # Safely retrieve the request from thread-local storage
        return getattr(_thread_local, 'request', None)
