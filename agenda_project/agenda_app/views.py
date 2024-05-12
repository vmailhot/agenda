from django.shortcuts import render, redirect
from . import models
from . import forms
import datetime


def home(request):
    calendars = models.Calendar.objects.all()
    events = models.Event.objects.all()

    # get month
    get_month = request.GET.get('month')
    if get_month:
        # get_month is a number
        month = datetime.datetime.strptime(get_month, "%m").strftime('%B')
    else:
        # get current month as a word
        month = datetime.datetime.now().strftime('%B')
        get_month = datetime.datetime.now().strftime('%m')

    # get year
    get_year = request.GET.get('year')
    if get_year:
        year = get_year
    else:
        year = datetime.datetime.now().strftime('%Y')

    
    if request.method == "POST":
        print("POST")
        form = request.POST
        print(form)
        # print all the id in the list of calendar_form of the POST request
        checkbox_values = request.POST.getlist('calendar_form')
        
        for calendar in calendars:
            if str(calendar.id) in checkbox_values:
                print("checked", calendar.id)
                calendar.checked = True
            else:
                calendar.checked = False
            calendar.save()

        return redirect("home")
    

    calendar_list = []
    for calendar in calendars:
        if calendar.checked:
            calendar_list.append(calendar.id)
    
 
    # get the calendar objects
    print("calendar_list", calendar_list)
    calendars_objects = models.Calendar.objects.filter(id__in=calendar_list)
    print("calendar_objects", calendars_objects)
    # get the events for the calendars
    events = models.Event.objects.filter(calendar__in=calendars_objects)

    # days dict for the month
    days = {}
    for i in range(1, 32):
        try:
            day = datetime.datetime(int(year), int(get_month), i)
            days[i] = day.strftime('%A')
        except ValueError:
            break
    
    week1 = []
    week2 = []
    week3 = []
    week4 = []
    week5 = []
    week6 = []

    current_week = 1
    count_days_in_week = 0
    seven_dict = {0: "Sunday", 1: "Monday", 2: "Tuesday", 3: "Wednesday", 4: "Thursday", 5: "Friday", 6: "Saturday"}
    for key, value in days.items():
        if value == "Sunday":
            current_week += 1
            count_days_in_week = 0

        # add blank days to first week
        if current_week == 1:
            print(count_days_in_week, current_week, key, value)
            if count_days_in_week == 0:
                if value == "Sunday":
                    week1.append({key: value})
                    count_days_in_week += 1
                elif value == "Monday":
                    to_add = 1
                elif value == "Tuesday":
                    to_add = 2
                elif value == "Wednesday":
                    to_add = 3
                elif value == "Thursday":
                    to_add = 4
                elif value == "Friday":
                    to_add = 5
                elif value == "Saturday":
                    to_add = 6
                for i in range(to_add):
                    week1.append({"": ""})
                    count_days_in_week += 1
                week1.append({key: value})
                count_days_in_week += 1
            else:
                week1.append({key: value})
                count_days_in_week += 1

        
        elif current_week == 2:
            week2.append({key: value})
            count_days_in_week += 1
        elif current_week == 3:
            week3.append({key: value})
            count_days_in_week += 1
        elif current_week == 4:
            week4.append({key: value})
            count_days_in_week += 1
        elif current_week == 5:
            week5.append({key: value})
            count_days_in_week += 1
        elif current_week == 6:
            week6.append({key: value})
            count_days_in_week += 1

    weeks_list = [week1, week2, week3, week4, week5, week6]



    return render(request, "agenda_app/home.html", {
        "calendars": calendars,
        "events": events,
        "month": month,
        "year": year,
        "days": days,
        "week1": week1,
        "week2": week2,
        "week3": week3,
        "week4": week4,
        "week5": week5,
        "week6": week6,
        "weeks_list": weeks_list,
    })

def event_detail(request, event_id):
    event = models.Event.objects.get(id=event_id)
    form = forms.EventForm(instance=event)
    if request.method == "POST":
        form = forms.EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            print("form saved")
            return redirect("home")

    return render(request, "agenda_app/event_detail.html", {
        "event": event,
        "form": form
    })

def create_event(request):
    form = forms.EventForm()
    if request.method == "POST":
        form = forms.EventForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")

    return render(request, "agenda_app/create_event.html", {
        "form": form
    })

def update_calendar(request, calendar_id):
    calendar = models.Calendar.objects.get(id=calendar_id)
    form = forms.CalendarForm(instance=calendar)
    if request.method == "POST":
        form = forms.CalendarForm(request.POST, instance=calendar)
        if form.is_valid():
            form.save()
            return redirect("home")

    return render(request, "agenda_app/calendar_update.html", {
        "form": form
    })