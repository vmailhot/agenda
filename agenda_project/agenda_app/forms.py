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