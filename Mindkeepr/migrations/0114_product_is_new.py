# Generated by Django 3.1.14 on 2022-06-05 22:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Mindkeepr', '0113_componentproduct'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='is_new',
            field=models.BooleanField(default=False, null=True, verbose_name='Is new ?'),
        ),
    ]
