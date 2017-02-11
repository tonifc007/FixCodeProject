# -*- coding: utf 8 -*-
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

#isto resolve o problema de acentuação do django.
#LEMBRAR SEMPRE!


# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.
from .celery import app as celery_app