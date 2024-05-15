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

    def __str__(self):
        return self.name
