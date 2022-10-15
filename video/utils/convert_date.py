from django.utils import timezone


def convert_date(date):
    now = timezone.now()
    time_difference = now - date
    if time_difference.days >= 365:
        return str(time_difference.days // 365) + ' سال پیش'
    elif time_difference.days >= 30:
        return str(time_difference.days // 30) + ' ماه پیش'
    elif time_difference.days >= 7:
        return str(time_difference.days // 7) + ' هفته پیش'
    elif time_difference.seconds >= 86400:
        return str(time_difference.seconds // 86400) + ' روز پیش'
    elif time_difference.seconds >= 3600:
        return str(time_difference.seconds // 3600) + ' ساعت پیش'
    elif time_difference.seconds >= 60:
        return str(time_difference.seconds // 60) + ' دقیقه پیش'
    else:
        return 'لحظاتی پیش'
