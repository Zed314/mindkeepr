from django.contrib.postgres.operations import TrigramExtension
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
        ('Mindkeepr', '0098_auto_20220213_2256'),
    ]

    operations = [
        TrigramExtension(),
    ]