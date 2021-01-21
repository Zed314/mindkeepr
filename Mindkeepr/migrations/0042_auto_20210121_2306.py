# Generated by Django 3.0.5 on 2021-01-21 23:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('Mindkeepr', '0041_remove_userprofile_extra'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='children', to='Mindkeepr.Category'),
        ),
        migrations.AlterField(
            model_name='element',
            name='polymorphic_ctype',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polymorphic_mindkeepr.element_set+', to='contenttypes.ContentType'),
        ),
        migrations.AlterField(
            model_name='event',
            name='polymorphic_ctype',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polymorphic_mindkeepr.event_set+', to='contenttypes.ContentType'),
        ),
        migrations.AlterField(
            model_name='location',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='children', to='Mindkeepr.Location'),
        ),
    ]
