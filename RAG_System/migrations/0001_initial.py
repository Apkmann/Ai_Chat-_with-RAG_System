# Generated by Django 4.2 on 2024-05-22 08:28

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="RAGMessages",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=50)),
                ("chat_id", models.IntegerField(default=0)),
                (
                    "File",
                    models.FileField(
                        default=None,
                        max_length=300,
                        null=True,
                        upload_to="RAG_System//media//",
                    ),
                ),
                ("conversations_For_Ai", models.JSONField(default=list)),
                ("conversations_For_User", models.JSONField(default=list)),
            ],
        ),
    ]
