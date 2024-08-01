import logging
from django.utils import timezone
from datetime import timedelta
from .models import UserActivity1
import re

logger = logging.getLogger(__name__)

class ActivityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if request.user.is_authenticated:
            current_time = timezone.now()
            curriculum_pattern = re.compile(r'^/curriculum/\d+/[^/]+/(?P<lesson_name>[\w-]+)/$')

            try:
                last_activity_str = request.session.get('last_activity', None)
                if last_activity_str:
                    last_activity = timezone.datetime.fromisoformat(last_activity_str).replace(tzinfo=current_time.tzinfo)
                else:
                    last_activity = None

                last_page_visited = request.session.get('last_page_visited', None)

                if request.path == '/user_login/':
                    UserActivity1.objects.create(
                        user=request.user,
                        date=current_time,
                        login_time=current_time
                    )

                elif request.path == '/user_logout/':
                    try:
                        last_login_activity = UserActivity1.objects.filter(user=request.user, logout_time__isnull=True).order_by('-login_time').first()

                        if last_login_activity:
                            last_login_activity.logout_time = current_time
                            last_login_activity.total_time_spent = current_time - last_login_activity.login_time
                            last_login_activity.save()
                        else:
                            logger.warning(f'No active login activity found for user: {request.user.username}')
                    except Exception as e:
                        logger.error(f'Error updating logout time for user: {request.user.username}, error: {e}')

                elif curriculum_pattern.match(request.path):
                    match = curriculum_pattern.match(request.path)
                    lesson_name = match.group('lesson_name') if match else None

                    if lesson_name:
                        if last_activity:
                            time_spent = current_time - last_activity
                        else:
                            time_spent = timedelta(seconds=0)
                        
                        UserActivity1.objects.create(
                            user=request.user,
                            date=current_time,
                            page_visited=lesson_name,
                            curriculum_time_spent=time_spent
                        )
                    else:
                        logger.info(f'Non-lesson page visited: {request.path}')

                request.session['last_activity'] = current_time.isoformat()
                request.session['last_page_visited'] = request.path

            except Exception as e:
                logger.error(f'Error recording activity for user: {request.user.username}, error: {e}')

        return response
