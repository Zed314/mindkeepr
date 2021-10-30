# Generated by Django 3.0.5 on 2021-09-24 21:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Mindkeepr', '0057_auto_20210924_2051'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movie',
            name='first_genre',
        ),
        migrations.RemoveField(
            model_name='movie',
            name='second_genre',
        ),
        migrations.AlterField(
            model_name='moveevent',
            name='status',
            field=models.CharField(choices=[('RESERVED', 'Reserved'), ('FREE', 'Free')], max_length=200, verbose_name='Status'),
        ),
        migrations.AlterField(
            model_name='stockrepartition',
            name='status',
            field=models.CharField(choices=[('RESERVED', 'Reserved'), ('FREE', 'Free')], max_length=200, verbose_name='Status'),
        ),
    ]