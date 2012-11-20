# Python
import os
import uuid

# Django
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.db import models


def upload_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('rawdata', str(instance.user.id), filename)


class RawImage(models.Model):
    user = models.ForeignKey(
        User,
        editable = False)

    file = models.FileField(
        storage = FileSystemStorage(location = '/webserver/www'),
        upload_to = upload_path,
    )

    uploaded = models.DateTimeField(
        auto_now_add = True,
        editable = False,
    )
