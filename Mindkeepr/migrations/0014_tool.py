# Generated by Django 3.0.5 on 2020-08-04 21:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Mindkeepr', '0013_auto_20200802_1846'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tool',
            fields=[
                ('element_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='Mindkeepr.Element')),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('Mindkeepr.element',),
        ),
    ]
