from django.db import models


class Pizza(models.Model):
    nome = models.CharField(max_length=50)
