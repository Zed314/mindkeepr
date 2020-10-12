# Generated by Django 3.0.5 on 2020-08-07 18:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Mindkeepr', '0018_auto_20200807_1804'),
    ]

    operations = [
        migrations.AlterField(
            model_name='machine',
            name='status',
            field=models.CharField(choices=[('30REP', 'To be repared'), ('60OK', 'Working'), ('20INV', 'To be tested'), ('50MEH', 'Partially working'), ('40REF', 'To be refilled'), ('10TRA', 'To be disposed')], default='INV', max_length=5),
        ),
        migrations.AlterField(
            model_name='machine',
            name='status_comment',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Status comment'),
        ),
    ]
