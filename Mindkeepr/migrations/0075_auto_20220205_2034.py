# Generated by Django 3.0.5 on 2022-02-05 20:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Mindkeepr', '0074_auto_20220127_2306'),
    ]

    operations = [
        migrations.AddField(
            model_name='moviecase',
            name='is_new',
            field=models.BooleanField(blank=True, null=True, verbose_name='Is new'),
        ),
        migrations.AlterField(
            model_name='book',
            name='custom_id',
            field=models.IntegerField(unique=True, verbose_name='Custom id'),
        ),
    ]
