from django.db import models

# Create your models here.
class Author(models.Model):
    name = models.CharField(max_length=100)

class Book(models.Model):
    author = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    price = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.title
