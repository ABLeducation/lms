from django.db import models
from django.template.defaultfilters import slugify
from autoslug import AutoSlugField # type: ignore
# from django.contrib.auth.models import User
from users.models import User,user_profile_student
import os
from django.urls import reverse

# Create your models here.
class School(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(null=True, blank=True)
    
    class Meta:
        verbose_name_plural = '1. Schools'
    
    def __str__(self):
        return self.name
        
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
        
class Standard(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = AutoSlugField(populate_from=name,unique=True,null=True, default=None)
    description = models.TextField(max_length=500,blank=True)
    
    class Meta:
        verbose_name_plural = '1. Standards'

    def __str__(self):
        return self.name
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name) 
        super().save(*args, **kwargs)

def save_subject_image(instance, filename):
    upload_to = 'Images/'
    ext = filename.split('.')[-1]
    # get filename
    if instance.subject_id:
        filename = 'Subject_Pictures/{}.{}'.format(instance.subject_id, ext)
    return os.path.join(upload_to, filename)

class Subject(models.Model):
    subject_id = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100)
    slug = models.SlugField(null=True, blank=True)
    standard = models.ForeignKey(Standard, on_delete=models.CASCADE, related_name='subjects')
    image = models.ImageField(upload_to=save_subject_image, blank=True, verbose_name='Subject Image')
    description = models.TextField(max_length=500,blank=True)
    display_on_frontend = models.BooleanField(default=True, verbose_name="Display on Frontend")
    schools = models.ManyToManyField(School)
    
    class Meta:
        verbose_name_plural = '2. Subjects'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.subject_id)
        super().save(*args, **kwargs)
        
class AISubject(models.Model):
    subject_id = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100)
    slug = models.SlugField(null=True, blank=True)
    image = models.ImageField(upload_to=save_subject_image, blank=True, verbose_name='Coding Subject Image')
    description = models.TextField(max_length=500,blank=True)

    class Meta:
        verbose_name_plural = 'AISubjects'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.subject_id)
        super().save(*args, **kwargs)

def save_lesson_files(instance, filename):
    upload_to = 'Images/'
    ext = filename.split('.')[-1]
    # get filename
    if instance.lesson_id:
        filename = 'lesson_files/{}/{}.{}'.format(instance.lesson_id,instance.lesson_id, ext)
        if os.path.exists(filename):
            new_name = str(instance.lesson_id) + str('1')
            filename =  'lesson_images/{}/{}.{}'.format(instance.lesson_id,new_name, ext)
    return os.path.join(upload_to, filename)

class Lesson(models.Model):
    lesson_id = models.CharField(max_length=100, unique=True)
    Standard = models.ForeignKey(Standard, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User,on_delete=models.CASCADE,default="")
    created_at = models.DateTimeField(auto_now_add=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE,related_name='lessons')
    name = models.CharField(max_length=250)
    position = models.PositiveSmallIntegerField(verbose_name="Chapter no.")
    slug = models.SlugField(null=True, blank=True)
    video = models.FileField(upload_to=save_lesson_files,verbose_name="Video", blank=True, null=True)
    video1=models.URLField(verbose_name="Videos", max_length=300,default="",null=True,blank=True)
    ppt = models.FileField(upload_to=save_lesson_files,verbose_name="Presentations", blank=True)
    Notes = models.FileField(upload_to=save_lesson_files,verbose_name="Notes", blank=True)
    assessment=models.URLField(verbose_name="Assessment", max_length=300,default="",null=True,blank=True)
    display_on_frontend = models.BooleanField(default=True, verbose_name="Display on Frontend")
    schools = models.ManyToManyField(School)

    class Meta:
        ordering = ['position']
        verbose_name_plural = '3. Lessons'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('curriculum:lesson_list', kwargs={'slug':self.subject.slug, 'standard':self.Standard.slug})
        
class AILesson(models.Model):
    lesson_id = models.CharField(max_length=100, unique=True)
    created_by = models.ForeignKey(User,on_delete=models.CASCADE,default="")
    subject = models.ForeignKey(AISubject, on_delete=models.CASCADE,related_name='coding_lessons')
    name = models.CharField(max_length=250)
    position = models.PositiveSmallIntegerField(verbose_name="Chapter no.")
    slug = models.SlugField(null=True, blank=True)
    video = models.FileField(upload_to=save_lesson_files,verbose_name="CodingVideo", blank=True, null=True)

    class Meta:
        ordering = ['position']
        verbose_name_plural='AILessons'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class WorkingDays(models.Model):
    standard = models.ForeignKey(Standard, on_delete=models.CASCADE,related_name='standard_days')
    day = models.CharField(max_length=100)
    def __str__(self):
        return self.day

class TimeSlots(models.Model):
    standard = models.ForeignKey(Standard, on_delete=models.CASCADE,related_name='standard_time_slots')
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return str(self.start_time) + ' - ' + str(self.end_time) 

class SlotSubject(models.Model):
    standard = models.ForeignKey(Standard, on_delete=models.CASCADE,related_name='standard_slots')
    day = models.ForeignKey(WorkingDays, on_delete=models.CASCADE,related_name='standard_slots_days')
    slot = models.ForeignKey(TimeSlots, on_delete=models.CASCADE,related_name='standard_slots_time')
    slot_subject = models.ForeignKey(Subject, on_delete=models.CASCADE,related_name='standard_slots_subject')

    def __str__(self):
        return str(self.standard)+ ' - ' + str(self.day) + ' - ' + str(self.slot) + ' - ' + str(self.slot_subject)

class Comment(models.Model):
    lesson_name = models.ForeignKey(Lesson,null=True, on_delete=models.CASCADE,related_name='comments')
    comm_name = models.CharField(max_length=100, blank=True)
    # reply = models.ForeignKey("Comment", null=True, blank=True, on_delete=models.CASCADE,related_name='replies')
    author = models.ForeignKey(User,on_delete=models.CASCADE,default="")
    body = models.TextField(max_length=500)
    date_added = models.DateTimeField(auto_now_add=True)
        

    def save(self, *args, **kwargs):
        self.comm_name = slugify("comment by" + "-" + str(self.author) + str(self.date_added))
        super().save(*args, **kwargs)

    def __str__(self):
        return self.comm_name

    class Meta:
        ordering = ['-date_added']
        verbose_name_plural = '4. Comments'

class Reply(models.Model):
    comment_name = models.ForeignKey(Comment, on_delete=models.CASCADE,related_name='replies')
    reply_body = models.TextField(max_length=500)
    author = models.ForeignKey(User,on_delete=models.CASCADE,default="")
    date_added = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = '5. Replies'

    def __str__(self):
        return "reply to " + str(self.comment_name.comm_name)
        
class CodingSubject(models.Model):
    subject_id = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100)
    slug = models.SlugField(null=True, blank=True)
    image = models.ImageField(upload_to=save_subject_image, blank=True, verbose_name='AICoding Subject Image')
    description = models.TextField(max_length=500,blank=True)

    class Meta:
        verbose_name_plural = 'Coding Subjects'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.subject_id)
        super().save(*args, **kwargs)
        
class CodingLesson(models.Model):
    lesson_id = models.CharField(max_length=100, unique=True)
    created_by = models.ForeignKey(User,on_delete=models.CASCADE,default="")
    subject = models.ForeignKey(CodingSubject, on_delete=models.CASCADE,related_name='aicoding_lessons')
    name = models.CharField(max_length=250)
    position = models.PositiveSmallIntegerField(verbose_name="Chapter no.")
    slug = models.SlugField(null=True, blank=True)
    video = models.FileField(upload_to=save_lesson_files,verbose_name="AICodingVideo", blank=True, null=True)

    class Meta:
        ordering = ['position']
        verbose_name_plural='Coding Lessons'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)
        
class StudentResult(models.Model):
    student_id = models.ForeignKey(user_profile_student, on_delete=models.CASCADE)
    subject_id = models.ForeignKey(Subject, on_delete=models.CASCADE)
    marks = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
def save_mechanzo_file(instance, filename):
    upload_to = 'Images/'
    ext = filename.split('.')[-1]
    # get filename
    if instance.kit_id:
        filename = 'Mechanzo_File/{}.{}'.format(instance.kit_id, ext)
    return os.path.join(upload_to, filename)
    
class Mechanzo_kit_name(models.Model):
    kit_id=models.CharField(max_length=50)
    kit_name=models.CharField(max_length=50)
    slug = models.SlugField(null=True, blank=True)

    def __str__(self):
        return self.kit_name

class Mechanzo_model_name(models.Model):
    model_id=models.CharField(max_length=50)
    model_name=models.CharField(max_length=50)
    kit=models.ForeignKey(Mechanzo_kit_name, on_delete=models.CASCADE, related_name='mechanzo_models')
    slug = models.SlugField(null=True, blank=True)
    file=models.FileField(upload_to=save_mechanzo_file,verbose_name="Mechanzo", blank=True)

    def __str__(self):
        return self.model_name
        
class Topicwise_Marks(models.Model):
    student=models.ForeignKey(user_profile_student, on_delete=models.CASCADE)
    topic_name 	= models.ForeignKey(Lesson, on_delete=models.DO_NOTHING)
    marks=models.IntegerField(default=0)  
    
class LectureRating(models.Model):
    lecture = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(default=0)
    date_rated = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('lecture', 'user')
        

class TeacherSubject(models.Model):
    subject_id = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100)
    slug = models.SlugField(null=True, blank=True)
    image = models.ImageField(upload_to=save_subject_image, blank=True, verbose_name='Subject Image')
    description = models.TextField(max_length=500,blank=True)
    display_on_frontend = models.BooleanField(default=True, verbose_name="Display on Frontend")
    
    class Meta:
        verbose_name_plural = '2. Teacher Subjects'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.subject_id)
        super().save(*args, **kwargs)

class TeacherLesson(models.Model):
    lesson_id = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    subject = models.ForeignKey(TeacherSubject, on_delete=models.CASCADE,related_name='Teacher_lessons')
    name = models.CharField(max_length=250)
    position = models.PositiveSmallIntegerField(verbose_name="Chapter no.")
    slug = models.SlugField(null=True, blank=True)
    video=models.URLField(verbose_name="Videos", max_length=300,default="",null=True,blank=True)
    assessment=models.URLField(verbose_name="Assessment", max_length=300,default="",null=True,blank=True)
    display_on_frontend = models.BooleanField(default=True, verbose_name="Display on Frontend")

    class Meta:
        ordering = ['position']
        verbose_name_plural = '3. Teacher Lessons'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)
        