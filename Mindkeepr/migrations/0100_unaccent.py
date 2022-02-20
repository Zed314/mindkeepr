from django.contrib.postgres.operations import UnaccentExtension
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
        ('Mindkeepr', '0099_trigram'),
    ]

    operations = [
        UnaccentExtension(),
    ]