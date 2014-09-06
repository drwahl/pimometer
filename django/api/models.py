from django.db import models

class Api(models.Model):
    title = models.TextField()
    s1 = models.ListField(EmbeddedDocument())
    s2 = models.ListField(EmbeddedDocument())

# Create your models here.
