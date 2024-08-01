from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect,JsonResponse
from django.contrib import messages
from django.urls import reverse 
from django.contrib.auth.decorators import login_required
from curriculum.models import *
from users.models import *
from curriculum import views
from django.core.cache import cache
from django.contrib.admin.models import LogEntry
import datetime as dt
from .signals import succesful_logout
from assessment.models import *
from django.db.models import Q,Max
from django.core.exceptions import ObjectDoesNotExist

def principal_home(request,subject_id=None):
    user=request.user
    school_obj = user_profile_principal.objects.get(user=user)
    
    school=school_obj.school
    students=user_profile_student.objects.filter(school__icontains=school).count()
    teachers=user_profile_teacher.objects.filter(school__icontains=school).count()

    subjects=Subject.objects.all().count()

    unread_notifications = NotificationPrincipal.objects.filter(principal_id=school_obj, read=False).count()

    context={
        "total_student": students,
        "school":school,
        "unread_notifications":unread_notifications,
        "teachers":teachers,
        "subjects":subjects
    }
    return render(request, "principal_template/school_home_template.html", context)


def student_data_view(request):
    return render(request, 'school/student_view_attendance.html')

def student_view_data_post(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('users:attendance_data')
    else:
        # Getting all the Input Data
        grade= request.POST.get('grade')

        student_obj = user_profile_student.objects.filter(grade__iexact=grade)
        total_students=student_obj.count()

        context = {
            "student_obj": student_obj,
            "total_students":total_students
        }
        return render(request, 'school/student_data_gradewise.html', context)
    
def display_teachers(request):
    user=request.user
    school=User.objects.get(username=user)
    school_obj = user_profile_principal.objects.get(user=school)
    
    school=school_obj.school
    teachers=user_profile_teacher.objects.filter(school__icontains=school)

    return render(request, "principal_template/teachers_list.html", {"teachers":teachers})

def subject_list(request):
    subjects={"Junior Scratch":"1-2",
        "Science Kit":"2-9",
        "Scratch":"3-6",
        "Robotics": "4-9",
        "MIT App Inventor":"5-6",
        "3D Designing":"5-10",
        "Arduino": "7-10",
        "Python": "7-10",
        "Internet of Things":"9-12",
        "AI": "11-12",
        "Raspberry Pi":"11-12",}
 

    return render(request, "principal_template/subjects_list.html", {"subjects":subjects})

def school_feedback(request):
    school_obj = user_profile_principal.objects.get(user=request.user)
    feedback_data = FeedBackPrincipal.objects.filter(principal=school_obj)
    context = {
        "feedback_data": feedback_data,
        "school":school_obj
    }
    return render(request, 'principal_template/school_feedback.html', context)

def school_feedback_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method.")
        return redirect('users:school_feedback')
    else:
        feedback = request.POST.get('feedback_message')
        school_obj = user_profile_principal.objects.get(user=request.user)

        try:
            add_feedback = FeedBackPrincipal(principal=school_obj, feedback=feedback, feedback_reply="")
            add_feedback.save()
            # messages.success(request, "Feedback Sent.")
            return redirect('users:principal_feedback')
        except:
            messages.error(request, "Failed to Send Feedback.")
            return redirect('users:principal_feedback')
        
def notifications(request):
    user=request.user
    school=user_profile_principal.objects.get(user=user)
    notifications = NotificationPrincipal.objects.filter(principal_id=school).order_by('-id')
    return render(request, 'principal_template/notification.html', {'notifications': notifications,"school":school})

def mark_notification_as_read(request, id):
    notification = NotificationSchool.objects.get(id=id)
    notification.read = True
    notification.save()
    return redirect('users:school_feedback')


def leaderboard(request):
    school=user_profile_principal.objects.get(user=request.user)
    school_name=school.school
    # students=user_profile_student.objects.filter(school=school_name)
    max_results = Result.objects.values('user__user_profile_student__grade').annotate(max_score=Max('score'))
    overall_students = Result.objects.filter(user__user_profile_student__school__icontains=school_name).order_by('-score')[:5]

    # Initialize a dictionary to store top 3 students for each grade
    top_students_by_grade = {}

    # Iterate through each grade and get the top 3 students
    for grade_info in max_results:
        grade = grade_info['user__user_profile_student__grade']
        max_score = grade_info['max_score']
        
        # Get the top 3 students with the maximum score in each grade
        top_students = Result.objects.filter(
            user__user_profile_student__grade=grade,
            user__user_profile_student__school__icontains=school_name
        ).order_by('-score')[:3]

        # Add the top students to the dictionary
        top_students_by_grade[grade] = top_students

    return render(request, 'principal_template/leadership.html', {'top_students_by_grade': top_students_by_grade,"overall_students":overall_students,"school":school})

def student_report(request):
    school=user_profile_principal.objects.get(user=request.user)
    school_name=school.school
    students = user_profile_student.objects.filter(school__icontains=school_name)
    grades = Standard.objects.all()

    students_gradewise = []

    for grade in grades:
        students_for_grade = students.filter(grade=grade).order_by('first_name')
        total_number=len(students_for_grade)
        students_gradewise.append((grade, students_for_grade,total_number))

    search_query = request.GET.get('search', '')
    if search_query:
        students = students.filter(Q(first_name__icontains=search_query) | Q(last_name__icontains=search_query))
        students_gradewise = [] 

    context = {
        "students_gradewise": students_gradewise,
        "students":students,
        "search_query": search_query,
        "school":school
    }
    # if request.is_ajax():
    #     students_data = [{'grade': student.grade, 'student_name': student.first_name, 'student_id': student.user_id} for student in students]
    #     return JsonResponse({'students': students_data})
    
    return render(request, 'principal_template/view_report.html', context)


def student_report_gradewise(request,grade):
    school=user_profile_principal.objects.get(user=request.user)
    school_name=school.school
    query = request.GET.get('q')
    students = user_profile_student.objects.filter(grade=grade)
    student_schoolwise=students.filter(school__icontains=school_name).order_by('first_name')

    if query:
        students = students.filter(
            Q(first_name__icontains=query) | Q(last_name__icontains=query) 
        )
    
    context = {
        'grade': grade,
        'students': student_schoolwise,
        "school":school,
        'search_query': query
    }
    
    return render(request, 'principal_template/student_report_gradewise.html', context)

    
def student_detail_report(request,user_id):
    try:
        school=user_profile_principal.objects.get(user=request.user)
        users=user_profile_student.objects.get(user_id=user_id)
        user=User.objects.get(username=users)
        marks=Result.objects.filter(user=user)

        return render(request, "principal_template/details_mark.html",{"users":users,"marks":marks,"school":school})
    except ObjectDoesNotExist:
        # Handle the case when a matching object doesn't exist
        return HttpResponse("The requested data does not exist.")


def school_profile(request):
    user = User.objects.get(id=request.user.id)
    school = user_profile_principal.objects.get(user=user)

    context={
        "user": user,
        "school": school
    }
    return render(request, 'principal_template/school_profile.html', context)

def school_profile_update(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('users:principal_profile')
    else:
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        school_name = request.POST.get('school_name')
        password = request.POST.get('password')
        mobile= request.POST.get('mobile')
        logo = request.FILES.get('logo')

        try:
            customuser = User.objects.get(id=request.user.id)
            if password != None and password != "":
                customuser.set_password(password)
            customuser.save()

            school = user_profile_principal.objects.get(user=customuser.id)
            school.school=school_name
            school.mobile=mobile
            school.profile_pic=logo
            school.first_name=first_name
            school.last_name=last_name
            school.save()
            messages.success(request, "Profile Updated Successfully")
            return redirect('users:principal_profile')
        except:
            messages.error(request, "Failed to Update Profile")
            return redirect('users:principal_profile')