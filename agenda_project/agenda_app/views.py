from django.shortcuts import render, redirect
from . import models
from . import forms
import datetime
import random


def home(request):
    # get the calendars
    calendars = models.Calendar.objects.all()


    # get month
    get_month = request.GET.get('month')
    if get_month:
        # get_month is a number
        month = datetime.datetime.strptime(get_month, "%m").strftime('%B')
    else:
        # get current month as a word
        month = datetime.datetime.now().strftime('%B')
        get_month = datetime.datetime.now().strftime('%m')

    events = models.Event.objects.filter(date__month=get_month)
    print("events", events)


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
    events = models.Event.objects.filter(calendar__in=calendars_objects, date__month=get_month, date__year=year)

    # days dict for the month
    days = {}
    for i in range(1, 32):
        try:
            day = datetime.datetime(int(year), int(get_month), i)
            days[i] = day.strftime('%A')
        except ValueError:
            break

    # get the month as a number
    month_number = int(get_month)
    
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
        "month_number": month_number
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
        "form": form,
        "calendar": calendar
    })

def create_calendar(request):
    form = forms.CalendarForm()
    if request.method == "POST":
        form = forms.CalendarForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")

    return render(request, "agenda_app/create_calendar.html", {
        "form": form
    })

def delete_calendar(request, calendar_id):
    calendar = models.Calendar.objects.get(id=calendar_id)
    calendar.delete()
    return redirect("home")

def delete_event(request, event_id):
    event = models.Event.objects.get(id=event_id)
    event.delete()
    return redirect("home")

def change_month(request, mode, month, year):
    current_month = month
    if current_month == 1:
        if mode == "minus":
            month = 12
            year -= 1
        elif mode == "plus":
            month = 2
    elif current_month == 12:
        if mode == "minus":
            month = 11
        elif mode == "plus":
            month = 1
            year += 1
    elif mode == "plus":
        month = current_month + 1
    elif mode == "minus":
        month = current_month - 1
    return redirect(f"/?month={month}&year={year}")

def create_school_calendar(request):
    # duree d'un cycle
    duree_cycle = 9
    # n periodes par jour
    n_periodes = 4
    periodes_dict = {
        1 : ["8:00", "9:15"],
        2 : ["9:30", "10:45"],
        3 : ["11:00", "12:15"],
        4 : ["13:25", "14:40"]
    }
    # debut/fin annee scolaire
    debut = "2023-08-31"
    fin = "2023-10-31"

    # cree un dict avec tous les jours d'ecole possible entre debut et fin (pas de fin de semaine)
    jours = {}
    current_date = datetime.datetime.strptime(debut, "%Y-%m-%d")
    end_date = datetime.datetime.strptime(fin, "%Y-%m-%d")

    # congee list
    congees_list = ["2023-09-04", "2023-09-22", "2023-10-09", "2023-10-25"]

    n = 1
    while current_date <= end_date:
        if n == 10: n = 1
        if current_date.weekday() < 5:  # Monday to Friday
            current_date_formated = current_date.strftime("%Y-%m-%d")
            if current_date_formated in congees_list:
                pass
            else:
                jours[current_date_formated] = n
                n += 1
        current_date += datetime.timedelta(days=1)

    horaire = {}
    n_cycle = 0
    for date, jour in jours.items():
        if jour == 1:
            n_cycle += 1
            horaire[n_cycle] = [date]
        else:
            horaire[n_cycle].append(date)



    # liste des matieres
    liste_matieres = ["francais, anglais, histoire, math, science, art, ppp, edu"]    
    # horaire du cycle
    # {numero du cycle : {date1 : {p1 : matiere, p2 : matiere, p3 : matiere, p4 : matiere}, date2 : {p1 : matiere, p2 : matiere, p3 : matiere, p4 : matiere}}
    # {1 : {
    #            2023-08-31 : {
    #                           1 :"francais",
    #                           2 : "math",
    #                           3 : "histoire",
    #                           4 : "art",
    #                         },   
    #            2023-09-01 : {
    #                           1 :"ppp",
    #                           2 : "science",
    #                           3 : "francais",
    #                           4 : "edu",
    #                         }
    #        }

    print(horaire, "\n", "*"*50)
    horaire_cours = {}
    for cycle, dates in horaire.items():
        for date in dates:
            # get the matiere
            matiere_dict = {}
            for i in range(1, 5):
                matiere_dict[i] = "ppp"
            new_dict = {}
            new_dict[date] = matiere_dict
            if cycle not in horaire_cours:
                horaire_cours[cycle] = new_dict
            else:
                horaire_cours[cycle].update(new_dict)

    for key, value in horaire_cours.items():
        print(key, value)

    
    # handle the POST request with the forms.SchoolCalendarForm
    if request.method == "POST":
        form = forms.SchoolCalendarForm(request.POST)
        if form.is_valid():
            form.save()
            # get the last school calendar id
            school_calendar = models.SchoolCalendar.objects.last()
            return redirect("create_school_period", school_calendar.id)
    else:
        form = forms.SchoolCalendarForm()


    
    


    return render(request, "agenda_app/create_school_calendar.html", {
        "horaire_cours" : horaire_cours,
        "form": form
    })
    
def create_school_period(request, school_calendar_id):

    school_calendar = models.SchoolCalendar.objects.get(id=school_calendar_id)
    number_of_period_added = int(models.SchoolPeriod.objects.filter(school_calendar=school_calendar).count()) + 1
    if number_of_period_added >= school_calendar.n_period_day:
        return redirect("create_school_subject", school_calendar.id)
    if request.method == "POST":
        print("POST")
        form = forms.SchoolPeriodForm(request.POST)
        print(form)
        if form.is_valid():
            form.save()
            if models.SchoolPeriod.objects.filter(school_calendar=school_calendar).count() == school_calendar.n_period_day:
                return redirect("create_school_subject", school_calendar.id)
            return redirect("create_school_period", school_calendar.id)
    else:
        form = forms.SchoolPeriodForm()

    return render(request, "agenda_app/create_school_period.html", {
        "form": form,
        "school_calendar": school_calendar,
        "number_of_period_added": number_of_period_added
    })

def create_school_subject(request, school_calendar_id):
    if request.method == "POST":
        form = forms.SchoolSubjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("create_school_subject", school_calendar_id)
    else:
        form = forms.SchoolSubjectForm()
    return render(request, "agenda_app/create_school_subject.html", {
        "form": form,
        "school_calendar_id": school_calendar_id
    })

def create_school_day_off(request, school_calendar_id):
    if request.method == "POST":
        form = forms.SchoolDayOffForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("create_school_day_off", school_calendar_id)
    else:
        form = forms.SchoolDayOffForm()
    return render(request, "agenda_app/create_school_day_off.html", {
        "form": form,
        "school_calendar_id": school_calendar_id
    })

def create_school_schedule(request, school_calendar_id):
    if models.SchoolSchedule.objects.filter(school_calendar=school_calendar_id).count() >= models.SchoolCalendar.objects.get(id=school_calendar_id).n_day_cycle:
        return redirect("home")
    # get all the subjects
    school_calendar = models.SchoolCalendar.objects.get(id=school_calendar_id)
    school_subjects = models.SchoolSubject.objects.filter(school_calendar=school_calendar)
    school_periods = models.SchoolPeriod.objects.filter(school_calendar=school_calendar)

    try:
        n_day = models.SchoolSchedule.objects.filter(school_calendar=school_calendar).count() + 1
    
    except:
        n_day = 1

    # handel the POST request with the forms.SchoolScheduleForm
    if request.method == "POST":
        form = request.POST
        print(form)
        for field in form:
            print(field)
            # if the field start with "period_"
            if field.startswith("period_"):
                form_subject_id = form[field]
                form_period_id = field.split("_")[1]
        form_n_day = form["n_day"]
        form_school_calendar_id = form["school_calendar"]
        form_school_period = models.SchoolPeriod.objects.get(id=form_period_id)
        form_school_subject = models.SchoolSubject.objects.get(id=form_subject_id)
        models.SchoolSchedule.objects.create(
            n_day=form_n_day,
            school_calendar=models.SchoolCalendar.objects.get(id=form_school_calendar_id),
            school_period=form_school_period,
            school_subject=form_school_subject
        )
        return redirect("create_school_schedule", school_calendar_id)
    return render(request, "agenda_app/create_school_schedule.html", {
        "school_calendar": school_calendar,
        "school_subjects": school_subjects,
        "school_periods": school_periods,
        "n_day": n_day
    })

def day_off_list(request):
    day_off_list = []
    events = models.Event.objects.all()
    for event in events:
        if event.need_day_off:
            day_off_list.append(event)
    # sort the list
    day_off_list.sort(key=lambda x: x.date)

    return render(request, "agenda_app/day_off_list.html", {
        "day_off_list": day_off_list
    })

def create_day_off(request, event_id):
    event = models.Event.objects.get(id=event_id)
    if event.day_off_took:
        event.day_off_took = False
    else:
        event.day_off_took = True
    event.save()
    return redirect("day_off_list")
