# Generated by Django 3.0.5 on 2022-02-05 23:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Mindkeepr', '0077_auto_20220205_2301'),
    ]

    operations = [
        migrations.AlterField(
            model_name='days',
            name='day',
            field=models.IntegerField(choices=[(0, 'Monday'), (1, 'Tuesday'), (2, 'Wednesday'), (3, 'Thursday'), (4, 'Friday'), (5, 'Saturday'), (6, 'Sunday')], max_length=1),
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
