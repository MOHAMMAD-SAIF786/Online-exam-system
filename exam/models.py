from django.db import models
from django.contrib.auth.models import User 
# Create your models here.

class Exam(models.Model):
    title = models.CharField(max_length=100)
    duration = models.IntegerField(help_text="Time in minutes")

    start_time = models.DateTimeField(null=True, blank=True)
    entry_window = models.IntegerField(default=20)  # minutes

    def __str__(self):
        return self.title
    
    
class Question(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    question = models.TextField()
    option1 = models.CharField(max_length=200)
    option2 = models.CharField(max_length=200)
    option3 = models.CharField(max_length=200)
    option4 = models.CharField(max_length=200)
    correct_answer = models.IntegerField()

class Answer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    exam = models.ForeignKey('Exam', on_delete=models.CASCADE)
    question = models.ForeignKey('Question', on_delete=models.CASCADE)
    selected_option = models.CharField(max_length=10)

    selected_answer = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} -Q{self.question.id}"
    




  
