from user.models import Visitor


class VisitorService:
    VISITOR_ID_KEY = '__vid'

    @staticmethod
    def create_visitor(uuid, data):
        visitor, created = Visitor.objects.update_or_create(uuid=uuid, defaults=data)
        return visitor

    @classmethod
    def set_user_on_visitor(cls, request):
        uuid = request.COOKIES.get(cls.VISITOR_ID_KEY)
        Visitor.objects.update_or_create(uuid=uuid, defaults={'user': request.user})

    @classmethod
    def get_visitor(cls, request):
        visitor, created = Visitor.objects.get_or_create(uuid=request.COOKIES.get(cls.VISITOR_ID_KEY))
        return visitor
