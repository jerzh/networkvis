from django.db import models

# Create your models here.
class Setting(models.Model):
    SETTING_CHOICES = [
        ('empty', 'empty'),
        ('sample', 'sample'),
        ('main', 'main'),
    ]
    setting = models.CharField(max_length=100, choices=SETTING_CHOICES)

class Page(models.Model):
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=300)
    color = models.CharField(max_length=20)
    content = models.TextField()

# class Link(models.Model):
#     pass
