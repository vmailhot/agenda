from django.contrib import admin
from . import models

admin.site.register(models.Calendar)
admin.site.register(models.Event)
admin.site.register(models.SchoolCalendar)
admin.site.register(models.SchoolPeriod)
admin.site.register(models.SchoolSubject)
admin.site.register(models.SchoolDayOff)
