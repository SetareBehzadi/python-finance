from django.db import models


# Create your models here.

class Package(models.Model):
    title = models.CharField(max_length=48)
    price = models.PositiveIntegerField()
    description = models.TextField(blank=True)
    is_enable = models.BooleanField(default=True)
    days = models.PositiveSmallIntegerField()

    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class PackageAttribute(models.Model):
    package = models.ForeignKey(Package, related_name='attributes', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title
