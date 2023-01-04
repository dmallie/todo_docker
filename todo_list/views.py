from django.shortcuts import render, redirect
from . import models
from accounts.models import UserAccount
from datetime import datetime
from django.utils.safestring import mark_safe
# To authenticate login infomration
from django.contrib.auth.decorators import login_required
from .forms import CreateEventForm

# Create your views here.
@login_required(login_url = 'accounts:login')
def index(request):
# get the account holder of the current login
       user = request.user
# get today's day from datetime object
       today = datetime.today()
# based on today's value fetch the whole data from calendar table
       dates_in_month = models.Calendar.objects.filter(month=today.month,
                     year=today.year).order_by('day').values_list('week_day', 'slug')
# Instantiate empty lists to hold calendar objects of the whole month
       calendar_obj = []
       week_days = [0, 1, 2, 3, 4, 5, 6] #["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
       months = ['January', 'February', 'March', 'April','May','June','July','August','September','October','November','December']
# loop through values_in_month and append calendar objects to calendar_obj
       for a_date in dates_in_month:
              calendar_obj.append(models.Calendar.objects.get(slug=a_date[1]))
# get context dictionary objects
       context = {
              'user': user,
              'calendar_obj': calendar_obj,
              'week_days': week_days,
              'calendar_month': months[today.month - 1],
              'calendar_year': today.year,
              'today': str(today).split(" ")[0],
              'today_day': today.day,
              'current_month': True,
              'slug': calendar_obj[1].slug
       }
       return render(request, 'todo_list/index.html', context=context)
##############################################################################################
# 
@login_required(login_url = 'accounts:login')
def todo_list(request, slug):
# get the user object
       user_obj = request.user
# get calendar object with the slug value
       calendar_obj = models.Calendar.objects.get(slug=slug)
# get an event object associated with this user and this calendar object
       event_obj = models.Events.objects.filter(user=user_obj, calendar=calendar_obj).order_by("event_scheduled_to_begin")
# Prepare the context needed for the page
       context = {
              'slug': slug,
              'user': user_obj,
              'events': event_obj,
       }
       return render(request, 'todo_list/todo_list.html', context=context)
################################################################################
#############    CREATE NEW EVENT  #############################################
@login_required(login_url="accounts:login")
def create_event(request, slug):
# get user object
       user_obj = request.user
# get calendar object through slug values
       calendar_obj = models.Calendar.objects.get(slug=slug)
       if request.method == 'POST':
              forms = CreateEventForm(request.POST)
# fetch form values from html form
              if forms.is_valid():
                     title_input = forms.cleaned_data['event_title']
                     event_description = forms.cleaned_data['event_description']
                     event_starts = request.POST.get('starts')
                     event_ends = request.POST.get('ends')
# create event object
                     events = models.Events.objects.create(
                            event_scheduled_to_begin = event_starts,
                            event_scheduled_to_end = event_ends,
                            event_description = event_description,
                            event_title = title_input,
                            calendar = calendar_obj,
                            user = user_obj,
                     )
# save event object
                     events.save()
# after saving redirect page to schedule_list
              return redirect('todo_list:todo_list', slug=slug)

       else:
              forms = CreateEventForm()
       context = {
              'forms': forms,
              'slug':slug,
              'user': user_obj,
       }
       return render(request, 'todo_list/create_event.html', context=context)
################################################################################
#############    UPDATE VIEWS ##################################################
@login_required(login_url='accounts:login')
def edit_events(request, id):
# get event object through its id
       event_obj = models.Events.objects.get(id=id)
 # get user profile object
       user_obj = request.user

       if request.method == 'POST':
# fetch form object with all its instances
              form = CreateEventForm(request.POST, instance=event_obj)
# validate this form object
              if form.is_valid():
# fetch and assign the newly inputted fields
                     event_obj.event_title = form.cleaned_data['event_title']
                     event_obj.event_description = form.cleaned_data['event_description']
                     event_obj.event_scheduled_to_begin = request.POST.get('starts')
                     event_obj.event_scheduled_to_end = request.POST.get('ends')
# save event object
                     event_obj.save()

                     return redirect('todo_list:todo_list', slug=event_obj.calendar.slug)
       else:
# renders the form in html when it's rendered before we press the submit button
              form = CreateEventForm(instance=event_obj)
       context = {
              'form': form,
              'event_obj': event_obj,
              'user': user_obj,
       }
       return render(request, 'todo_list/edit_events.html',context=context)
################################################################################
#############    DETAIL VIEWS ##################################################
@login_required(login_url='accounts:login')
def details_page(request, id):
# get event object through its id
       event_obj = models.Events.objects.get(id=id)
# get UserAccount objects
       user_obj = request.user
# retieve each fields of event object
# pack it in a dictionary
       if event_obj is not None:
              context = {
                     'event_obj': event_obj,
                     'user_obj': user_obj,
              }
       else:
              return redirect('todo_list:todo_list', slug=event_obj.calendar.slug)
# render the details page
       return render(request, 'todo_list/details_page.html', context=context)
################################################################################
#############    DELETE VIEWS ##################################################
@login_required(login_url='accounts:login')
def delete_events(request, id):
# get event object through event_id
       event_obj = models.Events.objects.get(id=id)
# get the list of event objects scheduled for the same day
       event_obj_list = models.Events.objects.filter(calendar=event_obj.calendar)
       if request.method == 'POST':
# delete event object
              event_obj.delete()
# If there are other events scheduled for the same day then go to schedule_list page
              if event_obj_list.count() != 0:
                     return redirect('todo_list:todo_list', slug=event_obj_list[0].calendar )
              else:
# otherwise go to calendar page
                     return redirect('todo_list:index')
       context = {
              'event_obj': event_obj,
       }
       return render(request, 'todo_list/delete.html', context=context )
################################################################################
#############    NEXT MONTH ####################################################

def next_month(request, slug):
# get the account holder of the current login
       user = request.user
# get the values of the current month and year from slug value
       calendar_obj = models.Calendar.objects.get(slug=slug)
# extract current month and year from calendar_obj
       current_month = calendar_obj.month
       current_year = calendar_obj.year
# we then calculate next_month and next_year
       next_month = current_month + 1
       next_year = current_year
       if next_month > 12:
              next_month = 1
              next_year = current_year + 1
              if next_year > 2025:
                     next_year = datetime.today().year
# we can get dates and other info about next_month from Calendar object
       dates_in_next_month = models.Calendar.objects.filter(month = next_month,
                                   year = next_year).order_by('day').values_list('id')
# populate calendar_obj with calendar objects of dates in next month
       next_calendar_month = []
       for obj in dates_in_next_month:
              next_calendar_month.append(models.Calendar.objects.get(id = obj[0]))
# create a context object for the calendar
       months = ['January', 'February', 'March', 'April','May','June','July','August','September','October','November','December']
       week_days = [0, 1, 2, 3, 4, 5, 6] # each number represents week days 0 for monday, 1 for tuesday, 2 for wednesday, 3 for thursday
       context = {
              'user':      user,
              'calendar_obj':      next_calendar_month,      # this is for the calendar dates
              'week_days' :        week_days,
              'calendar_month':    months[next_month-1],  # To display the month of the calendar
              'calendar_year':     next_year,    # to know when the year for the next month
              'slug':              next_calendar_month[0].slug,             # for the arrows to get the slug value
              'today':             str(datetime.today()).split(" ")[0],
       }#month_first_day

       if context['slug'] == context['today']:
              print("good it works")
       return render(request, 'todo_list/index.html', context=context)
################################################################################
#############    PREVIOUS MONTH ################################################

def prev_month(request, slug):
# get the account holder of the current login
       user = request.user
# get calendar object of the slug value
       calendar_obj = models.Calendar.objects.get(slug=slug)
# extract current month and year from calendar_obj
       current_month = calendar_obj.month
       current_year = calendar_obj.year
# we then calculate prev_month and prev_year
       prev_month = current_month - 1
       prev_year = current_year
       if prev_month < 1:
              prev_month = 12
              prev_year = current_year - 1
              if prev_year < 2020:
                     prev_year = datetime.today().year
# we can get dates and other info about prev_month from Calendar object
       dates_in_prev_month = models.Calendar.objects.filter(month = prev_month,
                                   year = prev_year).order_by('day').values_list('id')
# populate calendar_obj with calendar objects of dates in next month
       prev_calendar_month = []
       for obj in dates_in_prev_month:
              prev_calendar_month.append(models.Calendar.objects.get(id = obj[0]))
# create a context object for the calendar
       months = ['January', 'February', 'March', 'April','May','June','July','August','September','October','November','December']
       week_days = [0, 1, 2, 3, 4, 5, 6] # each number represents week days 0 for monday, 1 for tuesday, 2 for wednesday, 3 for thursday
       context = {
              'user':      user,
              'calendar_obj':      prev_calendar_month,      # this is for the calendar dates
              'week_days' :        week_days,
              'calendar_month':    months[prev_month-1],  # To display the month of the calendar
              'calendar_year':     prev_year,    # to know when the year for the next month
              'slug':              prev_calendar_month[0].slug,             # for the arrows to get the slug value
              'today':             str(datetime.today()).split(" ")[0],
       }#month_first_day

       if context['slug'] == context['today']:
              print("good it works")
       return render(request, 'todo_list/index.html', context=context)
