# Generated by Django 3.0.5 on 2020-08-07 18:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Mindkeepr', '0017_auto_20200806_2131'),
    ]

    operations = [
        migrations.AddField(
            model_name='machine',
            name='status',
            field=models.CharField(choices=[('TRA', 'To be disposed'), ('REP', 'To be repared'), ('REF', 'To be refilled'), ('INV', 'To be tested'), ('MEH', 'Partially working'), ('OK', 'Working')], default='INV', max_length=3),
        ),
        migrations.AddField(
            model_name='machine',
            name='status_comment',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='status_comment'),
        ),
    ]
