from django.db import models
import os
import uuid

def user_directory_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format(uuid.uuid4().hex[:10], ext)
    return os.path.join("files", filename)

class Greeting(models.Model):
    when = models.DateTimeField("date created", auto_now_add=True)

class File(models.Model):
    id = models.AutoField(primary_key=True)
    file = models.FileField(upload_to=user_directory_path, null=True)
    original_name = models.CharField(max_length=150, verbose_name='Nombre original', blank=True)
