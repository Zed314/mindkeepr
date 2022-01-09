# Generated by Django 3.0.5 on 2021-12-31 23:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Mindkeepr', '0063_auto_20211219_2221'),
    ]

    operations = [
        migrations.AddField(
            model_name='borrowevent',
            name='effective_borrow_date',
            field=models.DateField(null=True, verbose_name='Effective borrow date'),
        ),
        migrations.AddField(
            model_name='borrowevent',
            name='effective_return_date',
            field=models.DateField(null=True, verbose_name='Effective return date'),
        ),
        migrations.AddField(
            model_name='borrowevent',
            name='state',
            field=models.CharField(choices=[('NOT_THERE', 'Non existant'), ('NOT_STARTED', 'Not started'), ('IN_PROGRESS', 'In progress'), ('DONE', 'Completed'), ('CANCELLED', 'Cancelled')], default='NOT_STARTED', max_length=11),
        ),
    ]