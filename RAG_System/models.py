from django.db import models

class RAGMessages(models.Model):
    title = models.CharField(max_length=50)
    chat_id = models.IntegerField(default=0)
    File = models.CharField(max_length=250)
    conversations_For_Ai = models.JSONField(default=list)
    conversations_For_User = models.JSONField(default=list)