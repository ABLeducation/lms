from django.db import models
from curriculum.models import *

# Create your models here.
class Ebook(models.Model):
    book_id=models.CharField(max_length=50, default="")
    title = models.CharField(max_length=200)
    slug = models.SlugField(null=True, blank=True)
    author = models.CharField(max_length=100)
    grade = models.ForeignKey(Standard, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Topic_name(models.Model):
    topic_id=models.CharField(max_length=50)
    lesson_name=models.CharField(max_length=50)
    book=models.ForeignKey(Ebook, on_delete=models.CASCADE, related_name='ebook_lessons')
    slug = models.SlugField(null=True, blank=True)
    # pdf = models.FileField(upload_to='ebooks/pdfs/')
    file=models.URLField(verbose_name="content", max_length=300,default="")

    def __str__(self):
        return self.lesson_name
