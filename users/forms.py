from django import forms
from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User
from django.db import transaction
from users.models import *
from django.core.exceptions import ValidationError

class studentsignupform(UserCreationForm):
    choices=[('Vivekanand School,Delhi','Vivekanand School,Delhi'),
             ('New Era Public School','New Era Public School'),
             ('Bhaurav Devras Saraswati Vidya Mandir, Noida','Bhaurav Devras Saraswati Vidya Mandir, Noida'),
             ('MM Public School,Karnal','MM Public School,Karnal'),
             ('International Sahaja Public School, Dharamshala','International Sahaja Public School, Dharamshala'),
             ('Sparsh Global School,Greater Noida','Sparsh Global School,Greater Noida'),
             ('JP International School,Greater Noida','JP International School,Greater Noida'),
             ('SPS,Sonipat','SPS,Sonipat'),
             ('Satya Prakash Public School, Jabalpur','Satya Prakash Public School, Jabalpur'),
             ('Blooming Dale School,Budaun','Blooming Dale School,Budaun')
            ]
    
    choices_grade=[('1','1'),('2','2'),('3','3'),('4','4'),('5','5'),
             ('6','6'),('7','7'),('8','8'),('9','9'),('10','10'),
             ('11','11'),('12','12')]
             
    choices_section=[('A','A'),('B','B'),('C','C'),('D','D'),('E','E'),('F','F'),
    ('G','G'),('H','H'),('I','I'),('J','J'),('K','K'),('L','L'),('M','M'),('N','N')]
             
    username=forms.CharField(min_length=5, max_length=150,required=True,label="Username")
    email=forms.EmailField(required=True,label="Email")
    password1=forms.CharField(widget=forms.PasswordInput,label="Password")
    password2=forms.CharField(widget=forms.PasswordInput(),label="Confirm Password")
    First_Name=forms.CharField(required=True,label="First Name")
    Middle_Name=forms.CharField(required=False,label="Middle Name")
    Last_Name=forms.CharField(required=True,label="Last Name")
    dob=forms.DateField(widget =forms.NumberInput(attrs={'type':'date'}),label="DOB")
    grade=forms.CharField(required=True,label="Grade",widget=forms.Select(attrs={'class': 'form-control'},choices=choices_grade))
    section=forms.CharField(required=True,label="Section",widget=forms.Select(attrs={'class': 'form-control'},choices=choices_section))
    school = forms.TypedChoiceField(
        choices=sorted(choices, key=lambda x: x[1]),
        coerce=str,
        required=True,
        label="School",
        widget=forms.Select(attrs={'class': 'form-control'}),
    )
    country=forms.CharField(required=False,label="Country")
    state=forms.CharField(required=False,label="State")
    city=forms.CharField(required=False,label="City")

    class Meta(UserCreationForm.Meta):
        model=User

    def username_clean(self):  
        username = self.cleaned_data['username'].lower()  
        new = user_profile_student.objects.filter(username = username)  
        if new.count():  
            raise ValidationError("User Already Exist")
            # print("User Already Exist")
        return username  

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError("Email already exists")
        return email  
  
    def clean_password2(self):  
        password1 = self.cleaned_data['password1']  
        password2 = self.cleaned_data['password2']  
  
        if password1 and password2 and password1 != password2:  
            raise ValidationError("Password don't match")  
        return password2 
        
    def __init__(self, *args, **kwargs):
        super(studentsignupform, self).__init__(*args, **kwargs)
        
        # self.fields['school'].choices = sorted(self.fields['school'].choices, key=lambda x: x[1])
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None
        self.fields['username'].help_text = None
        self.label_suffix = ""

    def save(self):
        user = super().save(commit=False)
        user.email=self.cleaned_data.get('email')
        user.is_student = True
        user.is_active=False
        user.save()
        student = user_profile_student.objects.create(user=user)
        student.username=self.cleaned_data.get('username')
        student.password1=self.cleaned_data.get('password1')
        student.first_name=self.cleaned_data.get('First_Name')
        student.middle_name=self.cleaned_data.get('Middle_Name')
        student.last_name=self.cleaned_data.get('Last_Name')
        student.grade=self.cleaned_data.get('grade')
        student.section=self.cleaned_data.get('section')
        student.school=self.cleaned_data.get('school')
        student.country=self.cleaned_data.get('country')
        student.state=self.cleaned_data.get('state')
        student.city=self.cleaned_data.get('city')
        student.profile_pic=self.cleaned_data.get('profile_pic')
        student.save()
        return user

class parentsignupform(UserCreationForm):  
    username = forms.CharField(min_length=5, max_length=150,label="Username")  
    email = forms.EmailField(label="Email")  
    password1 = forms.CharField(widget=forms.PasswordInput,label="Password")  
    password2 = forms.CharField(widget=forms.PasswordInput,label="Confirm Password")
    First_Name=forms.CharField(required=True,label="First Name")
    Middle_Name=forms.CharField(required=False,label="Middle Name")
    Last_Name=forms.CharField(required=True,label="Last Name")
    Mobile=forms.CharField(required=True,label="Mobile Number")

    class Meta(UserCreationForm.Meta):
        model=User

  
    def username_clean(self):  
        username = self.cleaned_data['username'].lower()  
        new = user_profile_parent.objects.filter(username = username)  
        if new.count():  
            raise ValidationError("User Already Exist")  
        return username  
  
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError("Email already exists")
        return email 
  
    def clean_password2(self):  
        password1 = self.cleaned_data['password1']  
        password2 = self.cleaned_data['password2']  
  
        if password1 and password2 and password1 != password2:  
            raise ValidationError("Password don't match")  
        return password2  
        
    def __init__(self, *args, **kwargs):
        super(parentsignupform, self).__init__(*args, **kwargs)
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None
        self.fields['username'].help_text = None
        self.label_suffix = ""
  
    def save(self):  
        user = super().save(commit=False)
        user.email=self.cleaned_data.get('email')
        user.is_parent = True
        user.is_active=False
        user.save()
        parent= user_profile_parent.objects.create(user=user) 
        parent.username=self.cleaned_data['username']  
        parent.password1=self.cleaned_data['password1'] 
        parent.first_name=self.cleaned_data['First_Name']
        parent.middle_name=self.cleaned_data['Middle_Name']
        parent.last_name=self.cleaned_data['Last_Name']
        parent.mobile=self.cleaned_data['Mobile']
        parent.save()
        return user 
        
class teachersignupform(UserCreationForm):
    
    choices=[('Vivekanand School,Delhi','Vivekanand School,Delhi'),
             ('New Era Public School','New Era Public School'),
             ('Bhaurav Devras Saraswati Vidya Mandir, Noida','Bhaurav Devras Saraswati Vidya Mandir, Noida'),
             ('MM Public School,Karnal','MM Public School,Karnal'),
             ('International Sahaja Public School, Dharamshala','International Sahaja Public School, Dharamshala'),
             ('Sparsh Global School,Greater Noida','Sparsh Global School,Greater Noida'),
             ('JP International School,Greater Noida','JP International School,Greater Noida'),
             ('SPS,Sonipat','SPS,Sonipat'),
             ('Satya Prakash Public School,Jabalpur','Satya Prakash Public School,Jabalpur'),
             ('Blooming Dale School,Budaun','Blooming Dale School,Budaun'),
             ('ST. Mary School','ST. Mary School'),
            ]
             
    choices_grade=[('1','1'),('2','2'),('3','3'),('4','4'),('5','5'),
             ('6','6'),('7','7'),('8','8'),('9','9'),('10','10'),
             ('11','11'),('12','12')]
             
    username = forms.CharField(min_length=5, max_length=150,label="Username")  
    email = forms.EmailField(label="Email")  
    password1 = forms.CharField(widget=forms.PasswordInput,label="Password")  
    password2 = forms.CharField(widget=forms.PasswordInput,label="Confirm Password")
    First_Name=forms.CharField(required=True,label="First Name")
    Middle_Name=forms.CharField(required=False,label="Middle Name")
    Last_Name=forms.CharField(required=True,label="Last Name")
    Mobile=forms.CharField(required=True,label="Mobile Number")
    grade=forms.CharField(required=False,label="Grade",widget=forms.Select(attrs={'class': 'form-control'},choices=choices_grade))
    school=forms.CharField(required=True,label="School",widget=forms.Select(attrs={'class': 'form-control'},choices=choices))

    class Meta(UserCreationForm.Meta):
        model=User
  
    def username_clean(self):  
        username = self.cleaned_data['username'].lower()  
        new = user_profile_teacher.objects.filter(username = username)  
        if new.count():  
            raise ValidationError("User Already Exist")  
        return username  
  
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError("Email already exists")
        return email 
  
    def clean_password2(self):  
        password1 = self.cleaned_data['password1']  
        password2 = self.cleaned_data['password2']  
  
        if password1 and password2 and password1 != password2:  
            raise ValidationError("Password don't match")  
        return password2  
    
    def __init__(self, *args, **kwargs):
        super(teachersignupform, self).__init__(*args, **kwargs)
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None
        self.fields['username'].help_text = None
        self.label_suffix = ""
  
    def save(self):  
        user = super().save(commit=False)
        user.email=self.cleaned_data.get('email')
        user.is_teacher = True
        user.is_active=False
        user.save()
        teacher= user_profile_teacher.objects.create(user=user) 
        teacher.username=self.cleaned_data['username']  
        teacher.password1=self.cleaned_data['password1'] 
        teacher.first_name=self.cleaned_data['First_Name']
        teacher.middle_name=self.cleaned_data['Middle_Name']
        teacher.last_name=self.cleaned_data['Last_Name']
        teacher.mobile=self.cleaned_data['Mobile']
        teacher.grade=self.cleaned_data['grade']
        teacher.school=self.cleaned_data['school']
        teacher.save()
        return user


class principalsignupform(UserCreationForm): 
    
    choices=[('Vivekanand School,Delhi','Vivekanand School,Delhi'),
             ('New Era Public School','New Era Public School'),
             ('Bhaurav Devras Saraswati Vidya Mandir, Noida','Bhaurav Devras Saraswati Vidya Mandir, Noida'),
             ('MM Public School,Karnal','MM Public School,Karnal'),
             ('International Sahaja Public School, Dharamshala','International Sahaja Public School, Dharamshala'),
             ('Sparsh Global School,Greater Noida','Sparsh Global School,Greater Noida'),
             ('JP International School,Greater Noida','JP International School,Greater Noida'),
             ('SPS,Sonipat','SPS,Sonipat'),
             ('Satya Prakash Public School,Jabalpur','Satya Prakash Public School,Jabalpur'),
             ('Blooming Dale School,Budaun','Blooming Dale School,Budaun')
            ]
             
    username = forms.CharField(min_length=5, max_length=150,label="Username")  
    email = forms.EmailField(label="Email")  
    password1 = forms.CharField(widget=forms.PasswordInput,label="Password")  
    password2 = forms.CharField(widget=forms.PasswordInput,label="Confirm Password")
    First_Name=forms.CharField(required=True,label="First Name")
    Middle_Name=forms.CharField(required=False,label="Middle Name")
    Last_Name=forms.CharField(required=True,label="Last Name")
    Mobile=forms.CharField(required=True,label="Mobile Number")
    school=forms.CharField(required=True,label="School",widget=forms.Select(attrs={'class': 'form-control'},choices=choices))

    class Meta(UserCreationForm.Meta):
        model=User
  
    def username_clean(self):  
        username = self.cleaned_data['username'].lower()  
        new = user_profile_principal.objects.filter(username = username)  
        if new.count():  
            raise ValidationError("User Already Exist")  
        return username  
  
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError("Email already exists")
        return email 
  
    def clean_password2(self):  
        password1 = self.cleaned_data['password1']  
        password2 = self.cleaned_data['password2']  
  
        if password1 and password2 and password1 != password2:  
            raise ValidationError("Password don't match")  
        return password2  
    
    def __init__(self, *args, **kwargs):
        super(principalsignupform, self).__init__(*args, **kwargs)
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None
        self.fields['username'].help_text = None
        self.label_suffix = ""
  
    def save(self):  
        user = super().save(commit=False)
        user.email=self.cleaned_data.get('email')
        user.is_principal = True
        user.is_active=False
        user.save()
        principal= user_profile_principal.objects.create(user=user) 
        principal.username=self.cleaned_data['username']  
        principal.password1=self.cleaned_data['password1'] 
        principal.first_name=self.cleaned_data['First_Name']
        principal.middle_name=self.cleaned_data['Middle_Name']
        principal.last_name=self.cleaned_data['Last_Name']
        principal.mobile=self.cleaned_data['Mobile']
        principal.school=self.cleaned_data['school']
        principal.save()
        return user

class schoolsignupform(UserCreationForm):
    
    choices=[('Vivekanand School,Delhi','Vivekanand School,Delhi'),
             ('New Era Public School','New Era Public School'),
             ('Bhaurav Devras Saraswati Vidya Mandir, Noida','Bhaurav Devras Saraswati Vidya Mandir, Noida'),
             ('MM Public School,Karnal','MM Public School,Karnal'),
             ('International Sahaja Public School, Dharamshala','International Sahaja Public School, Dharamshala'),
             ('Sparsh Global School,Greater Noida','Sparsh Global School,Greater Noida'),
             ('JP International School,Greater Noida','JP International School,Greater Noida'),
             ('SPS,Sonipat','SPS,Sonipat'),
             ('Satya Prakash Public School,Jabalpur','Satya Prakash Public School,Jabalpur'),
             ('Blooming Dale School,Budaun','Blooming Dale School,Budaun'),
             ('ST. Mary School','ST. Mary School'),
            ]
             
    username=forms.CharField(min_length=5, max_length=150,required=True,label="Username")
    email=forms.EmailField(required=True,label="Email")
    password1=forms.CharField(widget=forms.PasswordInput(),label="Password")
    password2=forms.CharField(widget=forms.PasswordInput(),label="Confirm Password")
    School_Name=forms.CharField(required=True,label="School Name",widget=forms.Select(attrs={'class': 'form-control'},choices=choices))
    phone=forms.CharField(required=True,label="Phone Number")
    mobile=forms.CharField(required=True,label="Mobile Number")
    established=forms.DateField(widget =forms.NumberInput(attrs={'type':'date'}),label="Year of Establishment")
    country=forms.CharField(required=False,label="Country")
    state=forms.CharField(required=False,label="State")
    city=forms.CharField(required=False,label="City")
    pin=forms.CharField(required=True,label="Pincode")

    class Meta(UserCreationForm.Meta):
        model=User

    def username_clean(self):  
        username = self.cleaned_data['username'].lower()  
        new = user_profile_school.objects.filter(username = username)  
        if new.count():  
            raise ValidationError("User Already Exist")  
        return username  
  
    def email_clean(self):  
        email = self.cleaned_data['email'].lower()  
        new = user_profile_school.objects.filter(email=email)  
        if new.count():  
            raise ValidationError(" Email Already Exist")  
        return email  
  
    def clean_password2(self):  
        password1 = self.cleaned_data['password1']  
        password2 = self.cleaned_data['password2']  
  
        if password1 and password2 and password1 != password2:  
            raise ValidationError("Password don't match")  
        return password2 
    
    def __init__(self, *args, **kwargs):
        super(schoolsignupform, self).__init__(*args, **kwargs)
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None
        self.fields['username'].help_text = None
        self.label_suffix = ""

    def save(self):
        user = super().save(commit=False)
        user.email=self.cleaned_data.get('email')
        user.is_school= True
        user.is_active=False
        user.save()
        school = user_profile_school.objects.create(user=user)
        school.username=self.cleaned_data.get('username')
        school.password1=self.cleaned_data.get('password1')
        school.school_name=self.cleaned_data.get('School_Name')
        school.phone=self.cleaned_data.get('phone')
        school.mobile=self.cleaned_data.get('mobile')
        school.country=self.cleaned_data.get('country')
        school.state=self.cleaned_data.get('state')
        school.city=self.cleaned_data.get('city')
        school.pin=self.cleaned_data.get('pin')
        # school.district=self.cleaned_data.get('district')
        # school.principal=self.cleaned_data.get('principal')
        # school.mentor=self.cleaned_data.get('mentor')
        school.logo=self.cleaned_data.get('logo')
        school.save()
        return user

class LoginForm(forms.Form):
    username = forms.CharField(
        widget= forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    
class StudentProjectForm(forms.ModelForm):
    class Meta:
        model = StudentInnovativeProject
        fields = ['title', 'description', 'student_name', 'project_date', 'document', 'video_link']

        widgets = {
            'project_date': forms.DateInput(attrs={'class': 'datepicker'}),
        }

    def __init__(self, *args, **kwargs):
        super(StudentProjectForm, self).__init__(*args, **kwargs)
        self.label_suffix = ""
        
class MacroplannerForm(forms.ModelForm):
    choices_grade=[('1','1'),('2','2'),('3','3'),('4','4'),('5','5'),
             ('6','6'),('7','7'),('8','8'),('9','9'),('10','10'),
             ('11','11'),('12','12')]
    
    grade = forms.ChoiceField(choices=choices_grade, label='Grade')
    class Meta:
        model = Macroplanner
        fields = ['school','macroplanner','grade']
        widgets = {
            'school': forms.Select(attrs={'class': 'form-control'}),
        }


    def __init__(self, *args, **kwargs):
        super(MacroplannerForm, self).__init__(*args, **kwargs)
        self.fields['macroplanner'].required = True
        self.fields['macroplanner'].label = "Upload Planner"
        self.fields['macroplanner'].help_text = "PDF only"
        # Adding custom validation to ensure only PDF files are uploaded
        self.fields['macroplanner'].validators.append(self.validate_file_extension)

    def validate_file_extension(self, value):
        import os
        ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
        valid_extensions = ['.pdf']
        if not ext.lower() in valid_extensions:
            raise forms.ValidationError('Unsupported file extension. Please upload a PDF file.')
            
class MicroplannerForm(forms.ModelForm):
    MONTH_CHOICES = (
        ('January', 'January'),
        ('February', 'February'),
        ('March', 'March'),
        ('April', 'April'),
        ('May', 'May'),
        ('June', 'June'),
        ('July', 'July'),
        ('August', 'August'),
        ('September', 'September'),
        ('October', 'October'),
        ('November', 'November'),
        ('December', 'December'),
    )

    month = forms.ChoiceField(choices=MONTH_CHOICES, label='Month')

    class Meta:
        model = Microplanner
        fields = ['month', 'microplanner','school']


    def __init__(self, *args, **kwargs):
        super(MicroplannerForm, self).__init__(*args, **kwargs)
        self.fields['microplanner'].required = True
        self.fields['microplanner'].label = "Upload Planner"
        self.fields['microplanner'].help_text = "PDF only"
        # Adding custom validation to ensure only PDF files are uploaded
        self.fields['microplanner'].validators.append(self.validate_file_extension)

    def validate_file_extension(self, value):
        import os
        ext = os.path.splitext(value.name)[1]
        valid_extensions = ['.pdf']
        if not ext.lower() in valid_extensions:
            raise forms.ValidationError('Unsupported file extension. Please upload a PDF file.')
            
class DurationField(forms.MultiValueField):
    def __init__(self, *args, **kwargs):
        fields = (
            forms.IntegerField(),
            forms.IntegerField(),
        )
        super().__init__(fields, *args, **kwargs)

    def compress(self, data_list):
        if data_list:
            # Convert hours and minutes to total minutes
            hours = data_list[0] if data_list[0] else 0
            minutes = data_list[1] if data_list[1] else 0
            return hours * 60 + minutes
        return None

class DurationWidget(forms.MultiWidget):
    def __init__(self, attrs=None):
        widgets = (
            forms.NumberInput(attrs={'placeholder': 'Hours'}),
            forms.NumberInput(attrs={'placeholder': 'Minutes'}),
        )
        super().__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            hours = value // 60
            minutes = value % 60
            return [hours, minutes]
        return [None, None]
            
class AdvocacyVisitForm(forms.ModelForm):
    duration = DurationField(widget=DurationWidget())
    class Meta:
        model = AdvocacyVisit
        # fields = '__all__'
        exclude = ['verified_by', 'gallery','handling_comm_2']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'})
        }
        
        labels = {
            'name': 'Name of Mentor',
            'grade': 'Grade',
            'section': 'Section',
            'school': 'School Name',
            'date': 'Date of Visit',
            'topics': 'Topics Covered',
            'topics_microplanner': 'Topic as per Microplanner',
            'classroom_management': 'Classroom Management',
            'content_delievery': 'Content Delivery',
            'student_teacher_relation': 'Student-Teacher Relation',
            'dresscode': 'Dress Code',
            'handling_comm': 'Handling Communication(with School and HO)',
            'Regularity': 'Regularity',
            'Punctuality': 'Punctuality',
            'daily_report': 'Daily Report',
            'daily_progress_sheet': 'Daily Progress Sheet',
            'overall_behaviour': 'Overall Behaviour',
            'next_month_microplanner': 'Next Month Microplanner',
            'kreativityshow': 'Kreativity Show',
            'compiled_report': 'Compiled Report',
            'daily_win_sharing': 'Daily Win Sharing',
            'photo_video_recording': 'Photo/Video Recording',
            'name_advocacy': 'Name of Advocacy',
            'pedagogical_poweress': 'Pedagocical Prowess',
            'additional_info': 'No. of sessions, activities & Projects taken up this month class-wise?',
            'project_taken_club': 'Projects Taken in Innovation Club',
            'learning_outcomes': "Learning Outcome of today's class",
            'competition': 'Progress in Competition',
            'feedback': 'Feedback from Students',
            'improvement_tips': 'Feedback from Principal and Teachers',
            'remarks': 'Remarks',
        }
        
class TimetableForm(forms.ModelForm):
    class Meta:
        model=TimeTable
        fields=['school','file']
        widgets = {
            'school': forms.Select(attrs={'class': 'form-control'}),
        }
        
class InventoryForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = ['date', 'school', 'bill_of_materials']
        widgets = {
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'school': forms.Select(attrs={'class': 'form-control'}),
            'bill_of_materials': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

KIT_CHOICES = [
    ('Mechanz0 5+', 'Mechanz0 5+'),('Mechanz0 6+','Mechanz0 6+'),
    ('Mechanz0 9+','Mechanz0 9+'),('Mechanz0 11+','Mechanz0 11+'),
    ('Mechanz0 5+','Mechanz0 5+'),('Paper Circuit', 'Paper Circuit'),
    ('Arduino Uno', 'Arduino Uno'),('Jodo Straw','Jodo Straw'),
    ('Early Simple Machine','Early Simple Machine'),
    ('Arduino Nano','Arduino Nano'),('Arduino Mega','Arduino Mega'),
    ('Breadboard 400 pin','Breadboard 400 pin'),('Breadboard 800 pin','Breadboard 800 pin'),
    ('BO Motor - Straight','BO Motor - Straight'),
    ('BO Motor - L shape','BO Motor - L shape'),
    ('Motor driver L293D','Motor driver L293D'),
    ('Buzzer -Small','Buzzer -Small'),('Buzzer -Big','Buzzer -Big'),
    ('16x2 LCD display','16x2 LCD display'),
    ('I2C module for LCD','I2C module for LCD'),
    ('Uno USB Cables','Uno USB Cables'),('Nano USB Cable','Nano USB Cable'),
    ('Joy Stick module','Joy Stick module'),('9 Volt battery','9 Volt battery'),
    ('Keypad','Keypad'),('LDR Module','LDR Module'),
    ('Water Pump module','Water Pump module'),
    ('8*8 LED Matrix Module','8*8 LED Matrix Module'),('Bluetooth HC05','Bluetooth HC05'),('7 Segment Led Display','7 Segment Led Display'),
    ('MechanzO Motor','MechanzO Motor'),('BO Motor wheel','BO Motor wheel'),
    ('Node MCU','Node MCU'),('Hookup Wires ','Hookup Wires '),
    ('Jumper Male-Male','Jumper Male-Male'),('Jmper Male-Female','Jmper Male-Female'),
    ('Jumper Female-Female','Jumper Female-Female'),
    ('RGB LEDs','RGB LEDs'),('LEDs (Red)','LEDs (Red)'),
    ('LEDs (Green)','LEDs (Green)'),('LEDs (Blue)','LEDs (Blue)'),
    ('Push Button Switch 4 pin','Push Button Switch 4 pin'),('555 timer ic','555 timer ic'),('Capacitative Touch Switch','Capacitative Touch Switch'),
    ('Humidity Sensor','Humidity Sensor'),
    ('MQ-4 ','MQ-4 '),('MQ-135 ','MQ-135 '),('MQ-3','MQ-3'),
    ('Ultrasonic Sensor HC-SR-04','Ultrasonic Sensor HC-SR-04'),
    ('PIR Motion Detector Module','PIR Motion Detector Module'),('Soil Moisture Sensor','Soil Moisture Sensor'),('Touch Sensor','Touch Sensor'),
    ('Servo  Motor','Servo  Motor'),('Temperature Sensor','Temperature Sensor'),
    ('Rain Drop Sensor','Rain Drop Sensor'),
    ('IR sensor','IR sensor'),
    ('L298N','L298N'),
    ('Resistor Box','Resistor Box'),
]

class KitForm(forms.Form):
    kit_name = forms.ChoiceField(choices=KIT_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    quantity = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))

KitFormSet = forms.formset_factory(KitForm, extra=1)


# class CompetitionForm(forms.ModelForm):
#     class Meta:
#         model = Competition
#         fields = ['competition_name', 'venue', 'date', 'status', 'school']
#         widgets = {
#             'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
#             'school': forms.Select(attrs={'class': 'form-control'}),
#         }
class CompetitionForm(forms.ModelForm):
    GRADES = [(str(i), str(i)) for i in range(1, 13)]
    SECTIONS = [(chr(i), chr(i)) for i in range(65, 76)]

    STATUSES = [
        ('First', 'First'),
        ('Second', 'Second'),
        ('Third', 'Third'),
        ('Fourth', 'Fourth'),
        ('Fifth', 'Fifth')
    ]


    grade = forms.ChoiceField(choices=GRADES, widget=forms.Select(attrs={'class': 'form-control'}))
    section = forms.ChoiceField(choices=SECTIONS, widget=forms.Select(attrs={'class': 'form-control'}))
    status = forms.ChoiceField(choices=STATUSES, widget=forms.Select(attrs={'class': 'form-control', 'id': 'status'}))

    class Meta:
        model = Competition
        fields = ['competition_name', 'venue', 'date', 'status', 'school', 'grade', 'section', 'student']
        widgets = {
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'school': forms.Select(attrs={'class': 'form-control'}),
            'student': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['student'].queryset = user_profile_student.objects.none()

        if 'school' in self.data and 'grade' in self.data and 'section' in self.data:
            try:
                school = self.data.get('school')
                grade = self.data.get('grade')
                section = self.data.get('section')
                self.fields['student'].queryset = user_profile_student.objects.filter(
                    school=school, grade=grade, section=section
                ).order_by('first_name')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['student'].queryset = self.instance.school.user_profile_student_set.order_by('first_name')

GRADE_CHOICES=[
    ('1','1'),('2','2'),('3','3'),('4','4'),('5','5'),('6','6'),('7','7'),
    ('8','8'),('9','9'),('10','10'),('11','11'),('12','12'),
    ]
# class InnovationClubForm(forms.ModelForm):
#     class Meta:
#         model = InnovationClub
#         fields = ['name', 'grade', 'date', 'project_name','progress', 'school']
#         widgets = {
#             'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
#             'school': forms.Select(attrs={'class': 'form-control'}),
#             'grade': forms.Select(choices=GRADE_CHOICES, attrs={'class': 'form-control'}),
#         }
class InnovationClubForm(forms.ModelForm):
    GRADES = [(str(i), str(i)) for i in range(1, 13)]
    SECTIONS = [(chr(i), chr(i)) for i in range(65, 76)]

    PROGRESS_CHOICES = [
        ('0%', '0%'),
        ('25%', '25%'),
        ('50%', '50%'),
        ('75%', '75%'),
        ('100%', '100%'),
    ]

    grade = forms.ChoiceField(choices=GRADES, widget=forms.Select(attrs={'class': 'form-control'}))
    section = forms.ChoiceField(choices=SECTIONS, widget=forms.Select(attrs={'class': 'form-control'}))
    progress = forms.ChoiceField(choices=PROGRESS_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = InnovationClub
        fields = ['name', 'grade','section', 'date', 'project_name', 'progress', 'school']
        widgets = {
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'school': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.Select(attrs={'class': 'form-control'}),
            'project_name': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].queryset = user_profile_student.objects.none()

        if 'school' in self.data and 'grade' in self.data and 'section' in self.data:
            try:
                school = self.data.get('school')
                grade = self.data.get('grade')
                section = self.data.get('section')
                self.fields['name'].queryset = user_profile_student.objects.filter(
                    school=school, grade=grade, section=section
                ).order_by('first_name')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['name'].queryset = self.instance.school.user_profile_student_set.order_by('first_name')
        
class KreativityShowForm(forms.ModelForm):
    class Meta:
        model = KreativityShow
        fields = ['parent_name', 'child_name', 'date', 'grade','testimonial', 'school']
        widgets = {
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'school': forms.Select(attrs={'class': 'form-control'}),
        }

class GuestSessionForm(forms.ModelForm):
    class Meta:
        model = GuestSession
        fields = ['guest_name','date', 'gallery', 'school']
        widgets = {
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'school': forms.Select(attrs={'class': 'form-control'}),
        }
        
class StudentFilterForm(forms.Form):
    grade = forms.ChoiceField(
        choices=[('', 'All Grades')] + [(grade, grade) for grade in sorted(user_profile_student.objects.values_list('grade', flat=True).distinct())],
        required=False,
    )
    section = forms.ChoiceField(
        choices=[('', 'All Sections')] + [(section, section) for section in sorted(user_profile_student.objects.values_list('section', flat=True).distinct())],
        required=False,
    )