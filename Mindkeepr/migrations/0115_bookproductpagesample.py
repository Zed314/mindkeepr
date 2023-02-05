# Generated by Django 3.1.14 on 2023-01-29 11:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Mindkeepr', '0114_product_is_new'),
    ]

    operations = [
        migrations.CreateModel(
            name='BookProductPageSample',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=200, verbose_name='name')),
                ('file', models.FileField(upload_to='book_product_page_samples')),
                ('order', models.IntegerField()),
                ('book_product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='samples', to='Mindkeepr.bookproduct')),
            ],
        ),
    ]
