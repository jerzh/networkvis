from django.db import models
from django.contrib.postgres.fields import ArrayField


# the setting on the 'index' page (to decide which network to show)
class Setting(models.Model):
    SETTING_CHOICES = [
        ('empty', 'empty'),
        ('sample', 'sample'),
        ('main', 'main'),
    ]
    setting = models.CharField(max_length=100, choices=SETTING_CHOICES)


# ArrayField requires a function for default
def admin():
    return ['admin']


class Page(models.Model):
    title = models.CharField(max_length=30)
    # stores User id's
    authors = ArrayField(models.CharField(max_length=10), default=admin)
    description = models.CharField(max_length=300)
    color = models.CharField(max_length=20)
    desc_color = models.CharField(max_length=20, default='#444444')
    content = models.TextField()


class Link(models.Model):
    # stores Page id's
    source = models.CharField(max_length=10)
    target = models.CharField(max_length=10)
    color = models.CharField(max_length=20)


class User(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=100)
    # verbose_name = 'display name'
    name = models.CharField('display name', max_length=100)
