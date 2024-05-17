from django import forms
from . import models

class CalendarForm(forms.ModelForm):
    class Meta:
        model = models.Calendar
        fields = "__all__"


class EventForm(forms.ModelForm):
    class Meta:
        model = models.Event
        fields = "__all__"

class SchoolCalendarForm(forms.ModelForm):
    class Meta:
        model = models.SchoolCalendar
        fields = "__all__"

class SchoolPeriodForm(forms.ModelForm):
    class Meta:
        model = models.SchoolPeriod
        fields = "__all__"

class SchoolSubjectForm(forms.ModelForm):
    class Meta:
        model = models.SchoolSubject
        fields = "__all__"

class SchoolDayOffForm(forms.ModelForm):
    class Meta:
        model = models.SchoolDayOff
        fields = "__all__"