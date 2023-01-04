from django.shortcuts import render, redirect
from . import forms
from .models import UserAccount
from todo_list import models
# To authenticate the login information
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
# activation link packages
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
# email message packages
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
# datetime module
import datetime
# Create your views here.
def sign_up(request):
    if request.method == 'POST':
# create a form object
              form = forms.SignUpForm(request.POST)
# validate the information in the form
              if form.is_valid():
                     email = form.cleaned_data['email']
                     profile_picture = None
                     if len(request.FILES) != 0:
                            profile_picture = request.FILES['profile_img']
                     password = form.cleaned_data['password']
# # create a user account
#                    if profile_picture is None:
#                          profile_picture = "static/svg/user-solid.svg"
                     user = UserAccount.objects.create_user(
                            email, profile_picture, password
                     )
                     # form = forms.SignUpForm()
#Prepare the verificaton email
                     verification_content = {
                            'domain': get_current_site(request),
                            'user': request.user,
                            'token': default_token_generator.make_token(user),
                            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                     }
# the body part o the email
                     message = render_to_string('accounts/account_verification.html', verification_content)
# subject part of the email
                     subject = "activation link for TODO app"
# the destination email or user email address
                     to_email = email
# Compose the verification email
                     compose_email = EmailMessage(subject, message, to = [to_email])
# send the verification email
                     compose_email.send()

                     return redirect('/accounts/login/?command=verification&email='+to_email)        
    else:
        form = forms.SignUpForm()
    context = {
           'form_password': form['password'],
           'form_confirm' : form['confirm_password'],
           'form': form,
    }
    return render(request, 'accounts/sign_up.html', context=context)
# Activate the newly created account
def activate(request, uidb64, token):
# decode uid
       try:
              uid = urlsafe_base64_decode(uidb64).decode()
              user = UserAccount._default_manager.get(pk=uid)
       except(TypeError, ValueError, OverflowError, UserAccount.DoesNotExist):
              user = None
# decode  the token
       if user is not None and default_token_generator.check_token(user, token):
              user.is_active = True # activate the user account
              user.save()           # save the change
              messages.success(request, 'Congratulations! Your account is activated.')
              return redirect('accounts:login')
       else:
              messages.error(request, 'Activation link has expired')
              return redirect('accounts:sign_up')
#############################################################################################
# Login Page
def login(request):
       if request.method == 'POST':
# fetch the email address and password from the page
              email = request.POST.get('email')
              password = request.POST.get('password')
# authenticate the user using Django auth class
              user = auth.authenticate(email=email, password=password)
              print('user: ', user)
              if user is not None:
                     auth.login(request, user) # permit to login
                     messages.success(request, 'You are logged in') # prompt message conveying the success 
                     # url = request.META.get('HTTP_REFERER')
                     return redirect('todo_list:index')
              else:
                     messages.error(request, 'Invalid login credentials')
       return render(request, 'accounts/login.html')
############################################################################################
# Superuse Signup
def superuser_signup(request):
       if request.method == 'POST':
# create a form object
              form = forms.SignUpForm(request.POST)
# validate the information in the form
              if form.is_valid():
                     email = form.cleaned_data['email']
                     if len(request.FILES) != 0:
                            profile_picture = request.FILES['profile_img']
                     password = form.cleaned_data['password']
# create a user account
                     user = UserAccount.objects.create_superuser(
                            email, profile_picture, password
                     )
                     print('user in views.py: ', user)
                     form = forms.SignUpForm()
       else:
              form = forms.SignUpForm()
       context = {
              'form_password': form['password'],
              'form_confirm' : form['confirm_password'],
              'form': form,
       }
       return render(request, 'accounts/superuser_signup.html', context=context)
#################################################################################################
# To logout from the current account
@login_required(login_url='accounts:login')
def logout(request):
       auth.logout(request)
       messages.success(request, 'You are logged out')
       return redirect('accounts:login')
#################################################################################################
# Forgot Password page
def forgot_password(request):
       if request.method == 'POST':
# get email address
              email = request.POST.get('email')
# check if the email exists in our database
              if UserAccount.objects.filter(email=email).exists():
# if exists then get the owner of the email
                     user = UserAccount.objects.get(email__exact=email)
# send password reset link to the email
                     password_verification = {
                            'domain': get_current_site(request),
                            'user': user,
                            'token': default_token_generator.make_token(user),
                            'uid': urlsafe_base64_encode(force_bytes(user.id)),
                     }
                     print('password_verification[uid]: ', password_verification['uid'])
# prepare the body part of the email
                     email_body = render_to_string('accounts/reset_password_verification.html', password_verification)
# prepare the subject part of the email
                     subject = 'Password reset link for calendar app'
# user email address
                     to_email = email
# compose the email
                     compose_email = EmailMessage(subject, email_body, to=[to_email])
# send the email
                     compose_email.send()
                     return redirect('accounts:forgot_password')
              else:
                     messages.error(request, 'Email address doesnot exist in our database')
                     return redirect('accounts:forgot_password')
       return render(request, 'accounts/forgot_password.html')
# Notifying the user that the password resetting link has been sent
# def password_link_sent(request):

#        return render(request, 'accounts/after_forgot_password.html')
#################################################################################################
# decodes the Reset password link sent to our email
def activate_reset_password(request, uidb64, token):
# decode the uidb64 and get the user
       try:
              uid = urlsafe_base64_decode(uidb64).decode() # decodes the uidb64 & extract uid
              print('uid: ', uid)
# from the uid get the user object
              user = UserAccount.objects.get(id = uid)
       except (TypeError, ValueError, OverflowError, UserAccount.DoesNotExist):
              user = None
# decode the token
       if user is not None and default_token_generator.check_token(user, token):
# save the uid in the session and redirect the page to reset_password
              request.session['uid'] = uid
              messages.success(request, 'Please reset your password')
              return redirect('accounts:reset_password')
       else:
              messages.error(request, 'The link has been expired, please request a new one')
              return redirect('accounts:forgot_password')
#################################################################################################
# Reset the password
def reset_password(request):
       if request.method == 'POST':
# get password from reset page
              password_1 = request.POST.get('password')
              password_2 = request.POST.get('confirm_password')
# set the new password to the user
              if password_1 == password_2:
# get the user object from session
                     uid  = request.session.get('uid')
# get the user from its id
                     user = UserAccount.objects.get(pk = uid)
# set the new password and save the changes
                     user.set_password(password_1)
                     user.save()
                     messages.success(request,'The new password has been saved')
                     return redirect('accounts:login')
              else:
                     messages.error(request, 'Passwords do not match, Please retype again')
                     return redirect('accounts:reset_password')

       return render(request,'accounts/reset_password.html')
#################################################################################################
# My_profile page
@login_required(login_url = 'accounts:login')
def my_profile(request):
# get user infomration
    user = request.user    
# get all the schedules made by the user
    schedules = models.Events.objects.filter(user=user).order_by('event_scheduled_to_end')
# To change the profile picture
    if request.method == 'POST':
# get the profile picture
        if len(request.FILES) != 0:
            new_profile = request.FILES['edit_profile']
# save the changes         
            # userAcc = UserAccount()
            # userAcc.profile_pic = new_profile
            # userAcc.save()
            user.profile_pic = new_profile
            user.save()
# determine the status of each schedule
    now = datetime.datetime.now()
    status = {'completed': 0,
              'goingon': 0,
              'upcoming': 0,
              'total_schedules': 0}
    for each_event in schedules:
        start = each_event.event_scheduled_to_begin
        end = each_event.event_scheduled_to_end
# First we compare today's date with event date
        if str(now.date())  > str(each_event.calendar): # event is happened in the past
            status['completed'] += 1
        elif str(now.date()) < str(each_event.calendar): # event is not scheduled for today
            status['upcoming'] += 1
        else: # event is scheduled for today
# now we need to compare the time
            if now.time() > end: # event is completed
                status['completed'] += 1
            elif start <= now.time() <= end: # event is currently taking place
                status['goingon'] += 1
            else:
                print(each_event.event_title, ' is upcoming')      
                status['upcoming'] += 1
        status['total_schedules'] += 1
# prepare the context
    print('user.profile_pic: ', user.profile_pic)
    context = {
        'user' : user,
        'status' : status,
        }
    return render(request, 'accounts/my_profile.html', context)