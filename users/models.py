from django.db import models
from django.contrib.auth.models import AbstractUser
import os
from lms.settings import *
from django.core.validators import EmailValidator, MinLengthValidator,RegexValidator
from django.core.exceptions import ValidationError

# Create your models here.
class User(AbstractUser):
    is_student= models.BooleanField(default=False)
    is_parent= models.BooleanField(default=False)
    is_teacher= models.BooleanField(default=False)
    is_principal= models.BooleanField(default=False)
    is_school= models.BooleanField(default=False)
    
def save_profile_image(instance, filename):
    upload_to = 'Images/'
    ext = filename.split('.')[-1]
    # get filename
    if instance.user:
        filename = 'Profile_Pictures/{}.{}'.format(instance.user, ext)
    return os.path.join(upload_to, filename)

class user_profile_student(models.Model):
    mobile_number_pattern = r'^\+?[0-9]+$'
    mobile_number_validator = RegexValidator(
        regex=mobile_number_pattern,
        message="Enter a valid mobile number.",
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True,default="")
    first_name=models.CharField(max_length=50)
    middle_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    grade=models.CharField(max_length=50)
    section=models.CharField(max_length=50,default="")
    school=models.CharField(max_length=200,default="")
    country=models.CharField(max_length=100)
    state=models.CharField(max_length=50)
    city=models.CharField(max_length=50)
    mobile_number=models.CharField(max_length=20,validators=[mobile_number_validator],blank=True,null=True)
    marks_obtained=models.IntegerField(default=0)
    profile_pic=models.ImageField(upload_to=save_profile_image, blank=True, verbose_name='Profile Image')
    
    class Meta:
        verbose_name = 'User Profile Student'

    def __str__(self):
        return self.user.username

class user_profile_parent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True,default="")
    first_name=models.CharField(max_length=50)
    middle_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    mobile=models.CharField(max_length=15)
    
    class Meta:
        verbose_name = 'User Profile Parent'

    def __str__(self):
        return self.user.username

class user_profile_teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True,default="")
    first_name=models.CharField(max_length=50)
    middle_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    mobile=models.CharField(max_length=15)
    grade=models.IntegerField(null=True)
    school=models.CharField(max_length=200,default="")
    
    def get_escalation(self):
        if self.user.email in ['training1@thinnkware.com', 'training2@thinnkware.com','training10@thinnkware.com',
                               'training8@thinnkware.com','training5@thinnkware.com','training8@thinnkware.com','training9@thinnkware.com']:
            return 1
        else:
            return 2
            
    def get_profile(self):
        if self.user.email in ['training1@thinnkware.com', 'training2@thinnkware.com','training3@thinnkware.com','developer2@thinnkware.com',
                               'training4@thinnkware.com']:
            return "Sr. STEM Mentor"
        else:
            return "STEM Mentor"
        
    class Meta:
        verbose_name = 'User Profile Teacher'

    def __str__(self):
        return self.user.username

class user_profile_principal(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True,default="")
    first_name=models.CharField(max_length=50)
    middle_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    mobile=models.CharField(max_length=15)
    school=models.CharField(max_length=200,default="")
    profile_pic=models.ImageField(upload_to=save_profile_image, blank=True, verbose_name='Profile Image')
    
    class Meta:
        verbose_name = 'User Profile Principal'

    def __str__(self):
        return self.user.username

class user_profile_school(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True,default="")
    school_name=models.CharField(max_length=50,default="")
    phone=models.CharField(max_length=50,default="")
    mobile=models.CharField(max_length=15,default="")
    country=models.CharField(max_length=100,default="")
    state=models.CharField(max_length=50,default="")
    city=models.CharField(max_length=50,default="")
    street=models.CharField(max_length=100,default="")
    pin=models.CharField(max_length=50,default="")
    principal=models.CharField(max_length=100,default="")
    mentor=models.CharField(max_length=100,default="")
    district=models.CharField(max_length=100,default="")
    logo=models.ImageField(upload_to="logo/",default="")
    
    class Meta:
        verbose_name = 'User Profile School'

    def __str__(self):
        return self.user.username

class Contact(models.Model):
    name=models.CharField(max_length=50)
    contact_no=models.CharField(max_length=15)
    mail=models.EmailField(max_length=50)
    message=models.CharField(max_length=500)

    def __str__(self):
        return self.name
        
# Custom validator for a proper mobile number (10-digit format: "123-456-7890" or "1234567890")
def validate_mobile_number(value):
    # Remove any non-digit characters from the input
    cleaned_value = ''.join(filter(str.isdigit, value))

    # Check if the cleaned value is exactly 10 digits long
    if len(cleaned_value) != 10:
        raise ValidationError("Enter a valid 10-digit mobile number.")
        
class Enquiry(models.Model):
    name=models.CharField(max_length=50)
    contact=models.CharField(max_length=12,validators=[validate_mobile_number])
    email=models.EmailField(max_length=50,validators=[EmailValidator()])
    query=models.TextField()

    def __str__(self):
        return self.name
        
class Attendance(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    date=models.DateField()

class AttendanceReport(models.Model):
    # Individual Student Attendance
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(user_profile_student, on_delete=models.DO_NOTHING)
    attendance_id = models.ForeignKey(Attendance, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class FeedBackStudent(models.Model):
    id = models.AutoField(primary_key=True)
    student = models.ForeignKey(user_profile_student, on_delete=models.CASCADE)
    feedback = models.TextField()
    feedback_reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.student.first_name

class NotificationStudent(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(user_profile_student, on_delete=models.CASCADE)
    message = models.TextField()
    link = models.URLField(blank=True, null=True)
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.student_id.first_name
    
class UserLoginActivity(models.Model):
    # Login Status
    SUCCESS = 'S'
    FAILED = 'F'

    LOGIN_STATUS = ((SUCCESS, 'Success'),
                           (FAILED, 'Failed'))

    login_IP = models.GenericIPAddressField(null=True, blank=True)
    login_datetime = models.DateTimeField()
    login_username = models.CharField(max_length=40, null=True, blank=True)
    status = models.CharField(max_length=1, default=SUCCESS, choices=LOGIN_STATUS, null=True, blank=True)
    user_agent_info = models.CharField(max_length=255)
    login_num=models.CharField(max_length=1000,default=0)

    class Meta:
        verbose_name = 'user Login Activity'
        verbose_name_plural = 'user Login Activities'
        
    def get_student_name(self):
        try:
            student_profile = user_profile_student.objects.get(user__username=self.login_username)
            return f"{student_profile.first_name} {student_profile.last_name}"
        except user_profile_student.DoesNotExist:
            return None
        
    def get_grade(self):
        try:
            student_profile = user_profile_student.objects.get(user__username=self.login_username)
            grade=student_profile.grade
            return f"{grade}"
        except user_profile_student.DoesNotExist:
            return None
        
    def get_section(self):
        try:
            student_profile = user_profile_student.objects.get(user__username=self.login_username)
            section=student_profile.section
            return f"{section}"
        except user_profile_student.DoesNotExist:
            return None

    def __str__(self):
        return self.login_username
        
class UserActivity1(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField()
    login_time = models.DateTimeField(null=True, blank=True)
    logout_time = models.DateTimeField(null=True, blank=True)
    page_visited = models.CharField(max_length=255)
    curriculum_time_spent = models.DurationField(null=True, blank=True)
    time_spent = models.DurationField(null=True, blank=True)
    
    class Meta:
        verbose_name = 'user Acess Report'
        verbose_name_plural = 'user Acess Reports'

    def __str__(self):
        return f"{self.user.username} - {self.page_visited} on {self.date}"
        
class FeedBackSchool(models.Model):
    id = models.AutoField(primary_key=True)
    school= models.ForeignKey(user_profile_school, on_delete=models.CASCADE)
    feedback = models.TextField()
    feedback_reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.school.school_name
    
class NotificationSchool(models.Model):
    id = models.AutoField(primary_key=True)
    school_id = models.ForeignKey(user_profile_school, on_delete=models.CASCADE)
    message = models.TextField()
    link = models.URLField(blank=True, null=True)
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.school_id.school_name

class FeedBackPrincipal(models.Model):
    id = models.AutoField(primary_key=True)
    principal= models.ForeignKey(user_profile_principal, on_delete=models.CASCADE)
    feedback = models.TextField()
    feedback_reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.principal.school
        
class NotificationPrincipal(models.Model):
    id = models.AutoField(primary_key=True)
    principal_id = models.ForeignKey(user_profile_principal, on_delete=models.CASCADE)
    message = models.TextField()
    link = models.URLField(blank=True, null=True)
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.principal_id.school
        
class FeedBackTeacher(models.Model):
    id = models.AutoField(primary_key=True)
    teacher= models.ForeignKey(user_profile_teacher, on_delete=models.CASCADE)
    feedback = models.TextField()
    feedback_reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.teacher.first_name
    
class NotificationTeacher(models.Model):
    id = models.AutoField(primary_key=True)
    teacher_id = models.ForeignKey(user_profile_teacher, on_delete=models.CASCADE)
    message = models.TextField()
    link = models.URLField(blank=True, null=True)
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.teacher_id.first_name
        
class StudentInnovativeProject(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    student_name = models.CharField(max_length=100)
    project_date = models.DateField()
    document = models.FileField(upload_to='documents/')
    video_link = models.URLField()
    
    class Meta:
        verbose_name = 'Student Innovative Project'
    
class School(models.Model):
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='school_logos/')
    
    class Meta:
        verbose_name = "School's Logo"
    
class Macroplanner(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    grade=models.CharField(max_length=100,null=True,blank=True)
    school=models.CharField(max_length=100,choices=(
            ('Sparsh Global SChool,Greater Noida', 'Sparsh Global SChool,Greater Noida'),
            ('JP International School,Greater Noida', 'JP International School,Greater Noida'),
            ('SPS,Sonipat', 'SPS,Sonipat'),
            ('Vivekanand School,Delhi', 'Vivekanand School,Delhi'),
            ('Blooming Dale School,Budaun', 'Blooming Dale School,Budaun'),
            ('Satya Prakash Public School, Jabalpur','Satya Prakash Public School, Jabalpur'))
        )
    macroplanner=models.FileField(upload_to='macroplanner/')
    
    def __str__(self):
        return f"Macroplanner - User: {self.user.username}, File: {self.macroplanner.name}"
        
class Microplanner(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    month=models.CharField(max_length=100,default="")
    school=models.CharField(max_length=100,choices=(
            ('Sparsh Global SChool,Greater Noida', 'Sparsh Global SChool,Greater Noida'),
            ('JP International School,Greater Noida', 'JP International School,Greater Noida'),
            ('SPS,Sonipat', 'SPS,Sonipat'),
            ('Vivekanand School,Delhi', 'Vivekanand School,Delhi'),
            ('Blooming Dale School,Budaun', 'Blooming Dale School,Budaun'),
            ('Satya Prakash Public School, Jabalpur','Satya Prakash Public School, Jabalpur'))
        )
    microplanner=models.FileField(upload_to='microplanner/')
    
    def __str__(self):
        return f"Microplanner - User: {self.user.username}, File: {self.microplanner.name}"
        
class AdvocacyVisit(models.Model):
    name=models.CharField(max_length=100)
    grade=models.PositiveIntegerField(choices= [(i, str(i)) for i in range(1, 13)],default=1)
    section=models.CharField(max_length=1, choices=[(chr(i), chr(i)) for i in range(65, 76)],default="A")
    school=models.CharField(max_length=100,choices=(
            ('Sparsh Global SChool,Greater Noida', 'Sparsh Global SChool,Greater Noida'),
            ('JP International School,Greater Noida', 'JP International School,Greater Noida'),
            ('SPS,Sonipat', 'SPS,Sonipat'),
            ('Vivekanand School,Delhi', 'Vivekanand School,Delhi'),
            ('Blooming Dale School,Budaun', 'Blooming Dale School,Budaun'),
            ('Satya Prakash Public School, Jabalpur','Satya Prakash Public School, Jabalpur')),default=None
        )
    date=models.DateField()
    duration=models.CharField(max_length=50)
    topics=models.CharField(max_length=100)
    topics_microplanner = models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], default=False)
    classroom_management = models.IntegerField(
        choices=(
            (0, '0'),(1, '1'),(2, '2'),(3, '3'),(4, '4'),(5, '5')
        ),
        default=0
    )
    content_delievery=models.IntegerField(
        choices=(
            (0, '0'),(1, '1'),(2, '2'),(3, '3'),(4, '4'),(5, '5')
        ),
        default=0
    )

    student_teacher_relation=models.IntegerField(
        choices=(
            (0, '0'),(1, '1'),(2, '2'),(3, '3'),(4, '4'),(5, '5')
        ),
        default=0
    )
    dresscode=models.IntegerField(
        choices=(
            (0, '0'),(1, '1'),(2, '2'),(3, '3'),(4, '4'),(5, '5')
        ),
        default=0
    )
    handling_comm=models.IntegerField(
        choices=(
            (0, '0'),(1, '1'),(2, '2'),(3, '3'),(4, '4'),(5, '5')
        ),
        default=0
    )
    Regularity=models.IntegerField(
        choices=(
            (0, '0'),(1, '1'),(2, '2'),(3, '3'),(4, '4'),(5, '5')
        ),
        default=0
    )
    Punctuality=models.IntegerField(
        choices=(
            (0, '0'),(1, '1'),(2, '2'),(3, '3'),(4, '4'),(5, '5')
        ),
        default=0
    )
    daily_report=models.IntegerField(
        choices=(
            (0, '0'),(1, '1'),(2, '2'),(3, '3'),(4, '4'),(5, '5')
        ),
        default=0
    )
    daily_progress_sheet=models.IntegerField(
        choices=(
            (0, '0'),(1, '1'),(2, '2'),(3, '3'),(4, '4'),(5, '5')
        ),
        default=0
    )
    overall_behaviour=models.IntegerField(
        choices=(
            (0, '0'),(1, '1'),(2, '2'),(3, '3'),(4, '4'),(5, '5')
        ),
        default=0
    )
    next_month_microplanner=models.IntegerField(
        choices=(
            (0, '0'),(1, '1'),(2, '2'),(3, '3'),(4, '4'),(5, '5')
        ),
        default=0
    )
    kreativityshow=models.IntegerField(
        choices=(
            (0, '0'),(1, '1'),(2, '2'),(3, '3'),(4, '4'),(5, '5')
        ),
        default=0
    )
    compiled_report=models.IntegerField(
        choices=(
            (0, '0'),(1, '1'),(2, '2'),(3, '3'),(4, '4'),(5, '5')
        ),
        default=0
    )
    daily_win_sharing=models.IntegerField(
        choices=(
            (0, '0'),(1, '1'),(2, '2'),(3, '3'),(4, '4'),(5, '5')
        ),
        default=0
    )
    photo_video_recording=models.IntegerField(
        choices=(
            (0, '0'),(1, '1'),(2, '2'),(3, '3'),(4, '4'),(5, '5')
        ),
        default=0
    )
    pedagogical_poweress=models.TextField()
    additional_info=models.TextField()
    project_taken_club=models.TextField()
    learning_outcomes=models.TextField()
    competition=models.TextField()
    feedback=models.TextField()
    improvement_tips=models.TextField()
    remarks=models.TextField()
    name_advocacy=models.CharField(max_length=100)
    verified_by=models.BooleanField(default=False)
    gallery=models.URLField()

    def __str__(self):
        return self.name+' - '+self.school
        
class TimeTable(models.Model):
    school=models.CharField(max_length=100,choices=(
            ('Sparsh Global School,Greater Noida', 'Sparsh Global SChool,Greater Noida'),
            ('JP International School,Greater Noida', 'JP International School,Greater Noida'),
            ('SPS,Sonipat', 'SPS,Sonipat'),
            ('Vivekanand School,Delhi', 'Vivekanand School,Delhi'),
            ('Blooming Dale School,Budaun', 'Blooming Dale School,Budaun'),
            ('Satya Prakash Public School, Jabalpur', 'Satya Prakash Public School, Jabalpur')),default=None
        )
    file=models.FileField(upload_to='timetables/')

    def __str__(self):
        return self.school
        
class Inventory(models.Model):
    date = models.DateField()
    school = models.CharField(
        max_length=100,
        choices=(
            ('Sparsh Global School,Greater Noida', 'Sparsh Global School,Greater Noida'),
            ('JP International School,Greater Noida', 'JP International School,Greater Noida'),
            ('SPS,Sonipat', 'SPS,Sonipat'),
            ('Vivekanand School,Delhi', 'Vivekanand School,Delhi'),
            ('Blooming Dale School,Budaun', 'Blooming Dale School,Budaun'),
            ('Satya Prakash Public School, Jabalpur','Satya Prakash Public School, Jabalpur')
        )
    )
    challan_number = models.CharField(max_length=100)
    kits = models.JSONField(default=list)  # Store kits as a JSON list
    bill_of_materials = models.FileField(upload_to='bills/', blank=True, null=True)
    
    class Meta:
        verbose_name_plural = 'Inventories'

    def __str__(self):
        return f'{self.school} - {self.date} - {self.challan_number}'
    
class InnovationClub(models.Model):
    name=models.ForeignKey(user_profile_student, on_delete=models.CASCADE,null=True,blank=True)
    grade=models.CharField(max_length=100)
    section=models.CharField(max_length=100,null=True,blank=True)
    date = models.DateField(null=True, blank=True)
    project_name=models.CharField(max_length=100)
    progress=models.CharField(max_length=200)
    school=models.CharField(max_length=100,choices=(
            ('Sparsh Global School,Greater Noida', 'Sparsh Global SChool,Greater Noida'),
            ('JP International School,Greater Noida', 'JP International School,Greater Noida'),
            ('SPS,Sonipat', 'SPS,Sonipat'),
            ('Vivekanand School,Delhi', 'Vivekanand School,Delhi'),
            ('Blooming Dale School,Budaun', 'Blooming Dale School,Budaun'),
            ('Satya Prakash Public School, Jabalpur','Satya Prakash Public School, Jabalpur'))
        )
    
    def __str__(self):
        return f'{self.school} - {self.date}'


class Competition(models.Model):
    competition_name=models.CharField(max_length=100)
    venue=models.CharField(max_length=100)
    date=models.DateField()
    status=models.CharField(max_length=100)
    grade = models.CharField(max_length=50,null=True,blank=True)
    section = models.CharField(max_length=50,null=True,blank=True)
    student = models.ForeignKey(user_profile_student, on_delete=models.CASCADE,null=True,blank=True)
    school=models.CharField(max_length=100,choices=(
            ('Sparsh Global School,Greater Noida', 'Sparsh Global SChool,Greater Noida'),
            ('JP International School,Greater Noida', 'JP International School,Greater Noida'),
            ('SPS,Sonipat', 'SPS,Sonipat'),
            ('Vivekanand School,Delhi', 'Vivekanand School,Delhi'),
            ('Blooming Dale School,Budaun', 'Blooming Dale School,Budaun'),
            ('Satya Prakash Public School, Jabalpur','Satya Prakash Public School, Jabalpur'))
        )

    def __str__(self):
        return f'{self.school} - {self.date}'

class GuestSession(models.Model):
    date=models.DateField()
    guest_name=models.CharField(max_length=100)
    gallery=models.URLField()
    school=models.CharField(max_length=100,choices=(
            ('Sparsh Global School,Greater Noida', 'Sparsh Global SChool,Greater Noida'),
            ('JP International School,Greater Noida', 'JP International School,Greater Noida'),
            ('SPS,Sonipat', 'SPS,Sonipat'),
            ('Vivekanand School,Delhi', 'Vivekanand School,Delhi'),
            ('Blooming Dale School,Budaun', 'Blooming Dale School,Budaun'),
            ('Satya Prakash Public School, Jabalpur','Satya Prakash Public School, Jabalpur'))
        )
        
    def __str__(self):
        return f'{self.school} - {self.date}'
    
class KreativityShow(models.Model):
    date=models.DateField()
    parent_name=models.CharField(max_length=100)
    child_name=models.CharField(max_length=100)
    testimonial=models.URLField()
    grade=models.CharField(max_length=100)
    school=models.CharField(max_length=100,choices=(
            ('Sparsh Global School,Greater Noida', 'Sparsh Global SChool,Greater Noida'),
            ('JP International School,Greater Noida', 'JP International School,Greater Noida'),
            ('SPS,Sonipat', 'SPS,Sonipat'),
            ('Vivekanand School,Delhi', 'Vivekanand School,Delhi'),
            ('Blooming Dale School,Budaun', 'Blooming Dale School,Budaun'),
            ('Satya Prakash Public School, Jabalpur','Satya Prakash Public School, Jabalpur'))
        )
        
class SchoolContract(models.Model):
    school=models.CharField(max_length=100,choices=(
            ('Sparsh Global School,Greater Noida', 'Sparsh Global SChool,Greater Noida'),
            ('JP International School,Greater Noida', 'JP International School,Greater Noida'),
            ('SPS,Sonipat', 'SPS,Sonipat'),
            ('Vivekanand School,Delhi', 'Vivekanand School,Delhi'),
            ('Blooming Dale School,Budaun', 'Blooming Dale School,Budaun'),
            ('Satya Prakash Public School, Jabalpur','Satya Prakash Public School, Jabalpur'))
        )
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"Subscription for {self.school} from {self.start_date} to {self.end_date}"
        
class SchoolGallery(models.Model):
    school=models.CharField(max_length=100,choices=(
            ('Sparsh Global School,Greater Noida', 'Sparsh Global SChool,Greater Noida'),
            ('JP International School,Greater Noida', 'JP International School,Greater Noida'),
            ('SPS,Sonipat', 'SPS,Sonipat'),
            ('Vivekanand School,Delhi', 'Vivekanand School,Delhi'),
            ('Blooming Dale School,Budaun', 'Blooming Dale School,Budaun'),
            ('Satya Prakash Public School, Jabalpur','Satya Prakash Public School, Jabalpur'))
        )
    gallery = models.URLField()
    
    class Meta:
        verbose_name_plural = "School's Galleries"

    def __str__(self):
        return self.school
        
class ObservationSheet(models.Model):
    school=models.CharField(max_length=100,choices=(
            ('Sparsh Global School,Greater Noida', 'Sparsh Global SChool,Greater Noida'),
            ('JP International School,Greater Noida', 'JP International School,Greater Noida'),
            ('SPS,Sonipat', 'SPS,Sonipat'),
            ('Vivekanand School,Delhi', 'Vivekanand School,Delhi'),
            ('Blooming Dale School,Budaun', 'Blooming Dale School,Budaun'),
            ('Satya Prakash Public School, Jabalpur','Satya Prakash Public School, Jabalpur'))
        )
    observation_sheet = models.URLField()

    def __str__(self):
        return self.school
    
class CurriculumView(models.Model):
    school=models.CharField(max_length=100,choices=(
            ('Sparsh Global School,Greater Noida', 'Sparsh Global SChool,Greater Noida'),
            ('JP International School,Greater Noida', 'JP International School,Greater Noida'),
            ('SPS,Sonipat', 'SPS,Sonipat'),
            ('Vivekanand School,Delhi', 'Vivekanand School,Delhi'),
            ('Blooming Dale School,Budaun', 'Blooming Dale School,Budaun'),
            ('Satya Prakash Public School, Jabalpur','Satya Prakash Public School, Jabalpur'))
        )
    curriculum_sheet = models.URLField()

    def __str__(self):
        return self.school