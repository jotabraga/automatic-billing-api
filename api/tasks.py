from celery import shared_task


@shared_task
def my_task(arg1, arg2):

    # teste celery

    result = arg1 + arg2
    return result
