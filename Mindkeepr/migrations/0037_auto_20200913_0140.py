# Generated by Django 3.0.5 on 2020-09-13 01:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Mindkeepr', '0036_auto_20200912_2218'),
    ]

    operations = [
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
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('avatar', models.ImageField(upload_to='')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
