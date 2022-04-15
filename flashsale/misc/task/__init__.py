from __future__ import absolute_import
from flashsale.misc.task.CeleryTask import app as celery_app

print('__init__')

__all__ = ('celery_app',)
