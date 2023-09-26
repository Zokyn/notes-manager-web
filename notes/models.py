import datetime

from django.db import models
from django.utils import timezone

class Note(models.Model):
    note_title = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
    
    def __str__(self):
        return self.note_title

class Body(models.Model):
    note = models.ForeignKey(Note, on_delete=models.CASCADE)
    body_text = models.TextField(max_length=456)
    upvotes = models.IntegerField(default=0)
    def __str__(self):
        return self.body_text