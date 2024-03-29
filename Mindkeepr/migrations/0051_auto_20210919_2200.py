# Generated by Django 3.0.5 on 2021-09-19 22:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Mindkeepr', '0050_auto_20210919_1551'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='moviecase',
            options={},
        ),
        migrations.AddConstraint(
            model_name='moviecase',
            constraint=models.UniqueConstraint(fields=('custom_id', 'format_disk'), name='Unicity of custom id by format (DVD/Bluray)'),
        ),
    ]
