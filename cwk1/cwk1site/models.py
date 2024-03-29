from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Authors(models.Model):
    name = models.CharField(max_length=32)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__ (self):
        return self.name

class Stories(models.Model):
    headline = models.CharField(max_length=64)
    category = models.CharField(max_length=6, choices=[('pol', 'Politics'), ('art', 'Art'), ('tech', 'Technology'), ('trivia', 'Trivia')])
    region = models.CharField(max_length=10, choices=[('uk', 'UK'), ('eu', 'EU'), ('w', 'Worldwide')])
    author = models.ForeignKey(Authors, on_delete=models.CASCADE)
    date = models.DateField()
    details = models.CharField(max_length=128)

    def __str__ (self):
        return self.headline
