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
    desc_color = models.CharField(max_length=20, default='#444444')
    content = models.TextField()

class Link(models.Model):
    source = models.PositiveIntegerField()
    target = models.PositiveIntegerField()
    color = models.CharField(max_length=20)

class User(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=100)
    name = models.CharField('display name', max_length=100)
