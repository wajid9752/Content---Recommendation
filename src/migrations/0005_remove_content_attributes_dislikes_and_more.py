# Generated by Django 5.0.2 on 2024-02-09 06:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('src', '0004_content_attributes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='content_attributes',
            name='dislikes',
        ),
        migrations.RemoveField(
            model_name='content_attributes',
            name='likes',
        ),
    ]
