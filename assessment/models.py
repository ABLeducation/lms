from django.db import models
from users.models import *
from curriculum.models import School

# Create your models here.
class Quiz(models.Model):
    name=models.CharField(max_length=150)
    topic=models.CharField(max_length=150)
    grade=models.CharField(max_length=100, default=0)
    no_of_question=models.IntegerField()
    time=models.IntegerField(help_text="duration of the quiz in minutes")
    required_score_to_pass=models.IntegerField(help_text="required score to pass in %")
    schools = models.ManyToManyField(School)
    date=models.DateTimeField(default="")
    start_date = models.DateTimeField(blank=True,null=True)
    end_date = models.DateTimeField(blank=True,null=True)  

    def __str__(self):
        return f"{self.name}-{self.topic}"
    
    def get_questions(self):
        return self.question_set.all()
    
    class Meta:
        verbose_name_plural='Quizes'

class Question(models.Model):
    text=models.CharField(max_length=500)
    quiz=models.ForeignKey(Quiz, on_delete=models.CASCADE)
    created=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.text)
    
    def get_answers(self):
        return self.answer_set.all()

class Answer(models.Model):
    text=models.CharField(max_length=500)
    correct=models.BooleanField(default=False)
    question=models.ForeignKey(Question, on_delete=models.CASCADE)
    created=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"question-{self.question.text}, answer-{self.text}, correct-{self.correct}"
    
class Result(models.Model):
    quiz=models.ForeignKey(Quiz, on_delete=models.CASCADE)
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    score=models.FloatField()
    date_attempted = models.DateTimeField(auto_now_add=True, null=True,blank=True)

    def __str__(self):
        return str(self.user)