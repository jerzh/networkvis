# Generated by Django 2.1.7 on 2019-05-23 17:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogger', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='setting',
            name='setting',
            field=models.CharField(choices=[('empty', 'empty'), ('sample', 'sample')], max_length=100),
        ),
    ]
