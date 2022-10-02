# Generated by Django 3.0.5 on 2022-01-27 23:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Mindkeepr', '0073_element_ean'),
    ]

    operations = [
        migrations.AlterField(
            model_name='element',
            name='ean',
            field=models.CharField(max_length=13, null=True),
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
