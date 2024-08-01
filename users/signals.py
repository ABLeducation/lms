from django.contrib.auth.signals import user_logged_in,user_logged_out,user_login_failed
from django.db.models.signals import post_save,pre_save
from .models import *
from django.dispatch import receiver
import datetime as dt
from django.core.cache import cache
from django.core.mail import send_mail
from curriculum import models
import logging
from django.core.cache import cache
import inspect
from django.urls import reverse

@receiver(user_logged_out,sender=User)
def succesful_logout(sender,request,user,**kwargs):
    if 'last_logout' in request.session:
        ct_out=request.session.get('last_logout')
    else:
        request.session['last_logout']=str(dt.datetime.now())
        ct_out=request.session.get('last_logout')

    login_time=request.session.get('last_login')
    time_in=dt.datetime.strptime(login_time, '%Y-%m-%d %H:%M:%S.%f')
    time_out=dt.datetime.strptime(ct_out, '%Y-%m-%d %H:%M:%S.%f')

    time_out_minute=time_out.minute
    time_in_minute=time_in.minute
    absent=time_out_minute-time_in_minute

    if absent < 20:
        absent=cache.get('absent', 0,version=user.username)
        new_absent=absent+1
        cache.set('absent', new_absent, 60*60*24*365, version=user.username)
    else:
        present=cache.get('present', 0, version=user.username)
        new_present=present+1
        cache.set('present',new_present, 60*60*24*365, version=user.username) 


@receiver(post_save,sender=models.Subject)
def subject_added(sender,instance,created,**kwargs):
    if created:
        users=User.objects.all()
        for user in users: 
            if user.is_student:
                # send_mail("Subject added on LMS", "New subject added on LMS, you can start learning.", "lms@ableducation.com", [user.email])
                pass

@receiver(post_save,sender=models.Subject)
def lesson_added(sender,instance,created,**kwargs):
    if created:
        users=User.objects.all()
        for user in users: 
            if user.is_student:
                # send_mail("Subject added on LMS", "New lesson addedon LMS, you can start learning.", "lms@ableducation.com", [user.email])
                pass
                
error_log = logging.getLogger('error')


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


@receiver(user_logged_in)
def log_user_logged_in_success(sender, user, request, **kwargs):
    user=request.user
    ct=cache.get('count', 0, version=user.username)
    newcount=ct+1
    cache.set('count',newcount,60*60*24*365,version=user.username)

    request.session['last_login']=str(dt.datetime.now())

    try:
        user_agent_info = request.META.get('HTTP_USER_AGENT', '<unknown>')[:255],
        login_time=dt.datetime.now()
        login_count=cache.get('count',version=request.user.username)
        user_login_activity_log = UserLoginActivity(login_IP=get_client_ip(request),login_datetime=login_time,login_num=login_count,
                                                    login_username=user.username,
                                                    user_agent_info=user_agent_info,
                                                    status=UserLoginActivity.SUCCESS)
        user_login_activity_log.save()
    except Exception as e:
        # log the error
        error_log.error("log_user_logged_in request: %s, error: %s" % (request, e))


@receiver(user_login_failed)
def log_user_logged_in_failed(sender, credentials, request, **kwargs):
    try:
        user_agent_info = request.META.get('HTTP_USER_AGENT', '<unknown>')[:255],
        user_login_activity_log = UserLoginActivity(login_IP=get_client_ip(request),
                                                    login_username=credentials['username'],
                                                    user_agent_info=user_agent_info,
                                                    status=UserLoginActivity.FAILED)
        user_login_activity_log.save()
    except Exception as e:
        # log the error
        error_log.error("log_user_logged_in request: %s, error: %s" % (request, e))  
        
@receiver(post_save, sender=FeedBackStudent)
def comment_post_save(sender,instance,created, **kwargs):
    request=None
    for fr in inspect.stack():
        if fr[3] == 'get_response':
            request = fr[0].f_locals['request']
            break
    log_user = request.user
    student=user_profile_student.objects.get(user=log_user)
    message = f'{request.user} has given you response for your feedback "{instance.feedback}".'
    link = reverse('users:student_feedback')
    if instance.feedback_reply:
        notification = NotificationStudent(student_id=student, message=message, link=link)
        notification.save()
        
# @receiver(post_save, sender=FeedBackSchool)
# def school_comment_post_save(sender,instance,created, **kwargs):
#     import inspect
#     request=None
#     for fr in inspect.stack():
#         if fr[3] == 'get_response':
#             request = fr[0].f_locals['request']
#             break
#     log_user = request.user
#     school=user_profile_school.objects.get(user=log_user)
#     message = f'{request.user} has given you response for your feedback "{instance.feedback}".'
#     link = reverse('users:school_feedback')
#     if instance.feedback_reply:
#         notification = NotificationSchool(school_id=school, message=message, link=link)
#         notification.save()