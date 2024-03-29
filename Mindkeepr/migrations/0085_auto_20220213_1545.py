# Generated by Django 3.0.5 on 2022-02-13 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Mindkeepr', '0084_auto_20220213_1450'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='ean',
            field=models.CharField(max_length=13, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='moviecase',
            name='use_ean_as_effective_barcode',
            field=models.BooleanField(blank=True, default=True, null=True, verbose_name='Use ean as effective barcode'),
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
