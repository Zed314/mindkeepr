# Generated by Django 3.0.5 on 2020-08-15 23:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Mindkeepr', '0025_auto_20200808_2210'),
    ]

    operations = [
        migrations.CreateModel(
            name='PrintElement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(verbose_name='Quantity')),
                ('element', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Mindkeepr.Element')),
            ],
        ),
        migrations.CreateModel(
            name='PrintList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='Consumable',
        ),
        migrations.AddField(
            model_name='printelement',
            name='print_list',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='printelements', to='Mindkeepr.PrintList'),
        ),
    ]
