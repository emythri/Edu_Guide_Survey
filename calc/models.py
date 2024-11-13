from django.db import models
from django.contrib.auth.models import User

class Survey(models.Model):
    title = models.CharField(max_length=200)
    creator = models.ForeignKey(User, on_delete=models.CASCADE) #neww

    def __str__(self):
        return self.title

# class Question(models.Model):
#     survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name='questions')
#     text = models.CharField(max_length=200)
#     option_a = models.CharField(max_length=100)
#     option_b = models.CharField(max_length=100)
#     option_c = models.CharField(max_length=100)
#     option_d = models.CharField(max_length=100)

#     def __str__(self):
#         return self.text

class Question(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name='questions')
    text = models.CharField(max_length=200)

    def __str__(self):
        return self.text

