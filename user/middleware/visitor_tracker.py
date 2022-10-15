import re
import uuid

from user.services import VisitorService


class VisitorTrackerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        visitor_id = request.COOKIES.get(VisitorService.VISITOR_ID_KEY)
        pattern = r'^[0-9A-F]{8}-[0-9A-F]{4}-4[0-9A-F]{3}-[89AB][0-9A-F]{3}-[0-9A-F]{12}$'
        if not visitor_id:
            has_visitor_id = False
        elif not re.match(pattern=pattern, string=visitor_id.upper()):
            has_visitor_id = False
        else:
            has_visitor_id = True

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        if not has_visitor_id:
            visitor_id = uuid.uuid4()
            response.set_cookie(
                VisitorService.VISITOR_ID_KEY, visitor_id, max_age=10 * 52 * 7 * 24 * 60 * 60, samesite='lax'
            )
            print('cookies set to response:', visitor_id)
            data = self.get_client_data(request)
            VisitorService.create_visitor(visitor_id, data)

        return response

    @staticmethod
    def get_client_data(request):
        data = dict()
        data['user_id'] = request.user.id
        data['ip'] = request.META.get('REMOTE_ADDR')
        data['host'] = request.META.get('REMOTE_HOST')
        data['user_agent'] = request.META.get('HTTP_USER_AGENT')
        return data
