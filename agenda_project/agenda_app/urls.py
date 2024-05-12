from . import views
from django.urls import path

urlpatterns = [
    path('', views.home, name='home'),
    path('event/detail/<int:event_id>', views.event_detail, name='event_detail'),
    path('event/create', views.create_event, name='create_event'),
    path("calendar/update/<int:calendar_id>", views.update_calendar, name="update_calendar"),
]