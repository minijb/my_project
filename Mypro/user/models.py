from django.db import models


# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=30, unique=True)
    password = models.CharField(max_length=32)
    createtime = models.DateTimeField(auto_now_add=True)
    updatetime = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s_' % self.username


