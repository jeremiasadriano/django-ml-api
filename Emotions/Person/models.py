from django.db import models

# Create your models here.
class Person(models.Model):
    firstName = models.CharField(max_length=255)
    lastName = models.CharField(max_length=255)
    email = models.EmailField(max_length=120, unique=True)
    password = models.CharField(max_length=18)
class Message(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    phrase = models.CharField(max_length=255)
    answer = models.CharField(max_length=255)