# Generated by Django 4.2.1 on 2023-05-19 13:58

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("proxy", "0005_auto_20230519_0820"),
    ]

    operations = [
        migrations.RenameField(
            model_name="message",
            old_name="body",
            new_name="description",
        ),
    ]
