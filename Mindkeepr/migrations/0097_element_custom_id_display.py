# Generated by Django 3.0.5 on 2022-02-13 21:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Mindkeepr', '0096_auto_20220213_2148'),
    ]

    operations = [
        migrations.AddField(
            model_name='element',
            name='custom_id_display',
            field=models.CharField(max_length=6, null=True, unique=True),
        ),
    ]
