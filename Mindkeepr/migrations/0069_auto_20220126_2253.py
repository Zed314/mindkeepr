# Generated by Django 3.0.5 on 2022-01-26 22:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Mindkeepr', '0068_auto_20220126_2210'),
    ]

    operations = [
        migrations.AddField(
            model_name='element',
            name='barcode',
            field=models.CharField(max_length=13, null=True, unique=True),
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
