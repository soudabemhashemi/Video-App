from celery import shared_task


@shared_task
def event_collector():
    print('hey im event collector')
