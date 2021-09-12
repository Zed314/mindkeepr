# Generated by Django 3.0.5 on 2021-09-09 21:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Mindkeepr', '0046_auto_20210902_2235'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movie',
            name='summary',
        ),
        migrations.AddField(
            model_name='borrowevent',
            name='beneficiary',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='movie',
            name='budget',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='movie',
            name='original_language',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='movie',
            name='poster',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='movie',
            name='release_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='movie',
            name='remote_api_id',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='movie',
            name='trailer_video_url',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='movie',
            name='vote_average',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='movie',
            name='vote_count',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='moveevent',
            name='status',
            field=models.CharField(choices=[('FREE', 'Free'), ('RESERVED', 'Reserved')], max_length=200, verbose_name='Status'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='original_title',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='stockrepartition',
            name='status',
            field=models.CharField(choices=[('FREE', 'Free'), ('RESERVED', 'Reserved')], max_length=200, verbose_name='Status'),
        ),
    ]