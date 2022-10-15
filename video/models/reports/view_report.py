from django.db.models import Model, DateTimeField, ForeignKey, CASCADE


class ViewReport(Model):
    created_at = DateTimeField(auto_now_add=True)
    video = ForeignKey(to='video', on_delete=CASCADE, related_name='views')
    visitor = ForeignKey(to='user.Visitor', on_delete=CASCADE, related_name='views')
