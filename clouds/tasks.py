import celery

@celery.task(name='clouds.tasks.add')
def add():
    pass