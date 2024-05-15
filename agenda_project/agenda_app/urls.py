from . import views
from django.urls import path

urlpatterns = [
    path('', views.home, name='home'),
    path('event/detail/<int:event_id>', views.event_detail, name='event_detail'),
    path('event/create', views.create_event, name='create_event'),
    path('event/delete/<int:event_id>', views.delete_event, name='delete_event'),
    path("calendar/update/<int:calendar_id>", views.update_calendar, name="update_calendar"),
    path("calendar/create", views.create_calendar, name="create_calendar"),
    path("calendar/delete/<int:calendar_id>", views.delete_calendar, name="delete_calendar"),

    path("change_month/<str:mode>/<int:month>/<int:year>/", views.change_month, name="change_month"),

    path("create_school_calendar/", views.create_school_calendar, name="create_school_calendar")
]