# Generated by Django 4.2 on 2024-05-15 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Chatapp", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="chatmessages",
            name="title",
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
    ]
