# context_processors.py

from .models import Notification

def notifications_processor(request):
    if request.user.is_authenticated:
        notifications = Notification.objects.filter(user=request.user, is_read=False)
        return {'user_notifications': notifications}
    return {}

def unread_notifications(request):
    if request.user.is_authenticated:
        notifications = Notification.objects.filter(user=request.user, is_read=False)
    else:
        notifications = []
    return {'unread_notifications': notifications}