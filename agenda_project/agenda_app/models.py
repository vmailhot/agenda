from django.db import models

class Calendar(models.Model):
    name = models.CharField(max_length=100)
    checked = models.BooleanField(default=False)
    class ColorChoice(models.TextChoices):
        RED = 'Red'
        BLUE = 'Blue'
        GREEN = 'Green'
        YELLOW = 'Yellow'
        PURPLE = 'Purple'
        ORANGE = 'Orange'
        PINK = 'Pink'
        BROWN = 'Brown'
        GREY = 'Grey'
        BLACK = 'Black'
    color = models.CharField(
        max_length=6,
        choices=ColorChoice.choices,
        default=ColorChoice.RED,
    )

    def __str__(self):
        return self.name

class Event(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField()
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    calendar = models.ForeignKey(Calendar, on_delete=models.CASCADE)
    class ColorChoice(models.TextChoices):
        DEFAULT = 'Default'
        RED = 'Red'
        BLUE = 'Blue'
        GREEN = 'Green'
        YELLOW = 'Yellow'
        PURPLE = 'Purple'
        ORANGE = 'Orange'
        PINK = 'Pink'
        BROWN = 'Brown'
        GREY = 'Grey'
        BLACK = 'Black'

    color = models.CharField(
        max_length=7,
        choices=ColorChoice.choices,
        default=ColorChoice.RED,
    )
    need_day_off = models.BooleanField(default=False)
    day_off_took = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
class SchoolCalendar(models.Model):
    name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    n_day_cycle = models.IntegerField()
    n_period_day = models.IntegerField()

    def __str__(self):
        return self.name
    
class SchoolPeriod(models.Model):
    name = models.CharField(max_length=100)
    start_time = models.TimeField()
    end_time = models.TimeField()
    school_calendar = models.ForeignKey(SchoolCalendar, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
class SchoolSubject(models.Model):
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=7, default='#FF0000')
    school_calendar = models.ForeignKey(SchoolCalendar, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
class SchoolDayOff(models.Model):
    date = models.DateField()
    school_calendar = models.ForeignKey(SchoolCalendar, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.date} - {self.school_calendar}"
    
class SchoolSchedule(models.Model):
    n_day = models.IntegerField()
    school_calendar = models.ForeignKey(SchoolCalendar, on_delete=models.CASCADE)
    school_period = models.ForeignKey(SchoolPeriod, on_delete=models.CASCADE)
    school_subject = models.ForeignKey(SchoolSubject, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.school_period} - {self.school_subject}"

