# Generated by Django 3.2.9 on 2021-11-27 19:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='is_delete',
        ),
    ]
