# Generated by Django 3.0.5 on 2020-08-02 18:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Mindkeepr', '0012_auto_20200802_1814'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='attribute',
            name='Unique set of element and name',
        ),
    ]
