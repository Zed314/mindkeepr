# Generated by Django 3.0.5 on 2022-02-20 16:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Mindkeepr', '0100_unaccent'),
    ]

    operations = [
        migrations.CreateModel(
            name='BookAbstract',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=100, null=True)),
                ('summary', models.CharField(blank=True, max_length=1000, null=True)),
                ('nb_pages', models.IntegerField(blank=True, null=True)),
                ('release_date', models.DateField(blank=True, null=True)),
                ('cover', models.ImageField(blank=True, null=True, upload_to='book_images/cover')),
                ('author', models.CharField(blank=True, max_length=100, null=True)),
                ('author_2', models.CharField(blank=True, max_length=100, null=True)),
                ('publisher', models.CharField(blank=True, max_length=100, null=True)),
                ('open_library_api_id', models.CharField(blank=True, max_length=20, null=True)),
                ('ean', models.CharField(max_length=13, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='book',
            name='book_abstract',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='books', to='Mindkeepr.BookAbstract'),
        ),
    ]