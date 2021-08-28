from enum import unique
from django.db import models

# Create your models here.
Type = [
    ('speaker', 'speaker'),
    ('participant', 'participant') ]

class Conference(models.Model):
    title = models.CharField(max_length=256,blank=True,null=True)
    description = models.TextField(blank=True,null=True)
    start_date = models.DateTimeField(blank=True,null=True)
    end_date = models.DateTimeField(blank=True,null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.title

class People(models.Model):
    username = models.CharField(max_length=50,unique=True)
    email_id = models.EmailField(max_length = 254,unique = True)
    type = models.CharField(max_length=12,choices=Type,blank=True,null=True)

    def __str__(self) -> str:
        return self.email_id

class Talk(models.Model):
    conference_id = models.ForeignKey(Conference,on_delete=models.CASCADE,null=False)
    title = models.CharField(max_length=256,blank=True,null=True)
    description = models.TextField(blank=True,null=True)
    Duration_talk = models.DurationField(blank=True,null=True)
    date_time = models.DateTimeField(blank=True,null=True)
    public = models.ManyToManyField(People,blank=True,null=True)


    def __str__(self) -> str:
        return self.title