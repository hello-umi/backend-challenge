# Generated by Django 4.2.1 on 2023-05-17 18:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("proxy", "0002_channel_alter_message_dt_created_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="message",
            name="topic",
            field=models.ForeignKey(
                default=1, on_delete=django.db.models.deletion.PROTECT, to="proxy.topic"
            ),
            preserve_default=False,
        ),
    ]
