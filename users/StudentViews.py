from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.core.files.storage import FileSystemStorage #To upload Profile Picture
from django.urls import reverse
import datetime 
from django.contrib.auth.decorators import login_required
from assessment.models import *
from django.utils import timezone
from curriculum.models import *
from users.models import *
from django.core.cache import cache
from django.contrib.admin.models import LogEntry
import datetime as dt
from django.db.models import Q,Max,Count,F,Avg
from users.forms import *
from django.db.models import OuterRef, Subquery

def student_home(request,subject_id=None):
    user=request.user
    student=User.objects.get(username=user)
    student_obj = user_profile_student.objects.get(user=student)
    
    ct=cache.get('count', version=user.username)
    total_attendance = AttendanceReport.objects.filter(user=student_obj).count()
    attendance_present = AttendanceReport.objects.filter(user=student_obj, status=True).count()
    attendance_absent = AttendanceReport.objects.filter(user=student_obj, status=False).count()
    
    grade=student_obj.grade
    new_grade=grade[0]

    student_grade = Standard.objects.get(id=new_grade)
    total_subjects = Subject.objects.filter(standard_id=student_grade).count()

    subject_name = []
    data_present = []
    data_absent = []
    subject_data = Subject.objects.filter(standard_id=student_grade)
    for subject in subject_data:
        attendance = Attendance.objects.filter(id=subject.id)
        attendance_present_count = AttendanceReport.objects.filter(attendance_id__in=attendance, status=True,user=student_obj).count()
        attendance_absent_count =0
        subject_name.append(subject.name)
        data_present.append(attendance_present_count)
        data_absent.append(attendance_absent_count)

    logs=UserLoginActivity.objects.filter(login_username=request.user).count()

    count_absent=cache.get('absent', version=user.username)
    present_count=cache.get('present', version=user.username)

    unread_notifications = NotificationStudent.objects.filter(student_id=student_obj, read=False).count()
    
     # Get the user's score
    # user_score = Result.objects.filter(
    #     user=request.user
    # ).values('score').first()['score']
    
    user_result = Result.objects.filter(user=request.user).values('score').first()
    user_score = user_result['score'] if user_result is not None else None


    # Query to find the rank of the logged-in user within their grade
    # user_rank = Result.objects.filter(
    #     user__user_profile_student__grade=grade,
    #     score__gt=user_score 
    # ).count() + 1 
    
    # Calculate the user's rank if a score is available
    if user_score is not None:
        user_rank = Result.objects.filter(
        user__user_profile_student__grade=grade,
        score__gt=user_score
        ).count() + 1
    else:
        user_rank = None  # User has no score, so rank is also None
    
    average_score = Result.objects.filter(user=user).aggregate(Avg('score'))['score__avg']
    
    if average_score is not None:
        average_percentage = (average_score / 100) * 100
    else:
        average_percentage = 0
    
    quizzes = Quiz.objects.filter(start_date__lte=timezone.now(), end_date__gte=timezone.now())
    context={
        "total_attendance": total_subjects,
        "attendance_present": average_percentage,
        "attendance_absent": user_rank,
        "total_subjects": total_subjects,
        "subject_name": subject_name,
        "data_present": data_present,
        "data_absent": data_absent,
        "profile":student_obj,
        # "recent_visit":actionTime,
        "unread_notifications":unread_notifications,
        "logs":logs,
        "quizzes":quizzes
    }
    return render(request, "student_template/student_home_template.html", context)


def student_view_attendance(request):
    student = user_profile_student.objects.get(user=request.user.id) # Getting Logged in Student Data
    course = student.grade # Getting Course Enrolled of LoggedIn Student
    new_course=course[0]
    
    subjects = Subject.objects.filter(standard=new_course) # Getting the Subjects of Course Enrolled
    print(subjects)
    context = {
        "subjects": subjects,
        "profile":student
    }
    return render(request, "student_template/student_view_attendance.html", context)


def student_view_attendance_post(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('users:student_view_attendance')
    else:
        # Getting all the Input Data
        subject_id = request.POST.get('subject')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        # Parsing the date data into Python object
        start_date_parse = dt.datetime.strptime(start_date, '%Y-%m-%d')
        end_date_parse = dt.datetime.strptime(end_date, '%Y-%m-%d')

        subject_obj = Subject.objects.get(subject_id=subject_id)
        # Getting Logged In User Data
        user_obj = User.objects.get(username=request.user)
        # Getting Student Data Based on Logged in Data
        stud_obj = user_profile_student.objects.get(user=user_obj)

        logs=LogEntry.objects.filter(user=request.user)
        present_x=[]

        attendance = Attendance.objects.filter(user=user_obj)

        attendance_reports = AttendanceReport.objects.filter(attendance_id__in=attendance)

        for l in logs:
            if start_date_parse < l.action_time < end_date_parse:
                present_x.append(l.action_time)
                attendance_reports.status=True
            else:
                attendance_reports.status=False

        context = {
            "subject_obj": subject_obj,
            "attendance_reports": present_x
        }

        return render(request, 'student_template/student_attendance_data.html', context)


def student_profile(request):
    user = User.objects.get(id=request.user.id)
    student = user_profile_student.objects.get(user=user)

    context={
        "user": user,
        "student": student,
        "profile":student
    }
    return render(request, 'student_template/student_profile.html', context)


def student_profile_update(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('users:student_profile')
    else:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        middle_name= request.POST.get('middle_name')
        dob= request.POST.get('dob')
        grade= request.POST.get('grade')
        section= request.POST.get('section')
        school= request.POST.get('school')
        mobile=request.POST.get('mobile')
        profile_pic = request.FILES.get('profile_pic')

        try:
            customuser = User.objects.get(id=request.user.id)
            customuser.first_name = first_name
            customuser.last_name = last_name
            if password != None and password != "":
                customuser.set_password(password)
            customuser.save()

            student = user_profile_student.objects.get(user=customuser.id)
            student.dob=dob
            student.middle_name=middle_name
            student.grade=grade
            student.section=section
            student.school=school
            student.mobile_number=mobile
            student.profile_pic=profile_pic
            student.save()
            
            messages.success(request, "Profile Updated Successfully")
            return redirect('users:student_profile')
        except:
            messages.error(request, "Failed to Update Profile")
            return redirect('users:student_profile')

# def student_view_result(request):
#     student = user_profile_student.objects.get(admin=request.user.id)
#     student_result = StudentResult.objects.filter(student_id=student.id)
#     context = {
#         "student_result": student_result,
#         "profile":student
#     }
#     return render(request, "student_template/student_view_result.html", context)
    
    
def student_report(request):
    student=user_profile_student.objects.get(user=request.user)
    students=StudentResult.objects.filter(student_id=student)
    results=Result.objects.filter(user=request.user).order_by("-date_attempted")
    return render(request, 'student_template/studentreport.html', {'students': students,'results':results,"profile":student})
    
def student_feedback(request):
    student_obj = user_profile_student.objects.get(user=request.user)
    feedback_data = FeedBackStudent.objects.filter(student=student_obj)
    context = {
        "feedback_data": feedback_data,
        "profile":student_obj
    }
    return render(request, 'student_template/student_feedback.html', context)

def student_feedback_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method.")
        return redirect('users:student_feedback')
    else:
        feedback = request.POST.get('feedback_message')
        student_obj = user_profile_student.objects.get(user=request.user)

        try:
            add_feedback = FeedBackStudent(student=student_obj, feedback=feedback, feedback_reply="")
            add_feedback.save()
            messages.success(request, "Feedback Sent.")
            return redirect('users:student_feedback')
        except:
            messages.error(request, "Failed to Send Feedback.")
            return redirect('users:student_feedback')
    
def notifications(request):
    user=request.user
    student=user_profile_student.objects.get(user=user)
    notifications = NotificationStudent.objects.filter(student_id=student).order_by('-id')
    return render(request, 'student_template/notification.html', {'notifications': notifications,"profile":student})

def mark_notification_as_read(request, id):
    notification = NotificationStudent.objects.get(id=id)
    notification.read = True
    notification.save()
    return redirect('users:student_feedback')
    
def leaderboard(request):
    student = user_profile_student.objects.get(user=request.user)
    school = student.school
    user_grade = student.grade
    
    # Get the user's score safely
    user_result = Result.objects.filter(user=request.user).values('score').first()
    user_score = user_result['score'] if user_result else 0

    # Query to find the rank of the logged-in user within their grade safely
    if user_score > 0:
        user_rank = Result.objects.filter(
            user__user_profile_student__grade=user_grade,
            score__gt=user_score  # Count students with higher scores
        ).count() + 1  # Add 1 to get the user's rank
    else:
        user_rank = None

    # Handle max results if available
    max_results = Result.objects.values('user__user_profile_student__grade').annotate(max_score=Max('score'))

    # Get the top 5 students overall, safely handle empty results
    overall_students = Result.objects.all().order_by('-score')[:5] or None

    # Find the top 3 leaders of the student's grade safely
    grade_leaders = Result.objects.filter(
        user__user_profile_student__grade=user_grade
    ).order_by('-score')[:3] or None

    return render(request, 'student_template/leadership.html', {
        'top_students_by_grade': grade_leaders,
        "overall_students": overall_students,
        "school": school,
        "user_rank": user_rank,
        "user_grade": user_grade
    })
    
def subjects(request):
    student=user_profile_student.objects.get(user=request.user)
    grade=student.grade
    subjects=Subject.objects.filter(standard=grade)

    return render(request, "student_template/subjects.html", {"subjects":subjects})
    
def student_login_activity(request):
    user = request.user

    try:
        student_profile = user_profile_student.objects.get(user=user)
    except user_profile_student.DoesNotExist:
        return render(request, "school/no_permission.html", {"message": "You do not have permission to view this page."})

    login_usernames = [user.username]
    
    # Subquery to get the latest login datetime for the logged-in user
    latest_login_subquery = UserLoginActivity.objects.filter(login_username=OuterRef('login_username')).order_by('-login_datetime').values('login_datetime')[:1]
    
    # Get the latest login activity for the logged-in user
    latest_login_activities = UserLoginActivity.objects.filter(
        login_username__in=login_usernames,
        login_datetime=Subquery(latest_login_subquery)
    ).distinct().order_by('-login_datetime')

    # Include user ID in the context
    activities_with_user_id = [
        {
            'login_activity': activity,
            'user_id': User.objects.get(username=activity.login_username).id
        }
        for activity in latest_login_activities
    ]

    context = {
        "activities_with_user_id": activities_with_user_id,
        "student_profile": student_profile,
    }
    return render(request, "student_template/school_login_activity.html", context)


def student_activity_view(request, user_id):
    activities = UserActivity1.objects.filter(user=user_id).order_by('-date')
    context = {
        'activities': activities,
        'user_id': user_id
    }
    return render(request, 'student_template/student_activity.html', context)

def SampleProjectReport(request):
    student=user_profile_student.objects.get(user=request.user)
    school=student.school
    sampleproject=ProjectSample.objects.filter(school__icontains=school)
    print(f'project Sample-{sampleproject}')
    return render(request, "student_template/sampleproject.html",{'sampleproject': sampleproject})