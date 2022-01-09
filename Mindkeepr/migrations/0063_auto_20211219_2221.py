# Generated by Django 3.0.5 on 2021-12-19 22:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Mindkeepr', '0062_borrowevent_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='borrowevent',
            name='active',
            field=models.BooleanField(default='False'),
        ),
        migrations.AlterField(
            model_name='moveevent',
            name='status',
            field=models.CharField(choices=[('FREE', 'Free'), ('RESERVED', 'Reserved')], max_length=200, verbose_name='Status'),
        ),
        migrations.AlterField(
            model_name='stockrepartition',
            name='status',
            field=models.CharField(choices=[('FREE', 'Free'), ('RESERVED', 'Reserved')], max_length=200, verbose_name='Status'),
        ),
    ]