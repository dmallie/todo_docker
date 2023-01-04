from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
# Create your models here.
class AccountManager(BaseUserManager):
# To create a normal user account
       def create_user(self, email, profile_pic, password=None):
# if eamil is None then raise value error
              if email is None:
                     raise ValueError('Email isnot provided')
# else create a model object and assign it to user object
              user = self.model(
                     email          = self.normalize_email(email),
                     username       = email.split('@')[0],
                     profile_pic    = profile_pic,
              )
# set password using set_password method
              user.set_password(password)
# save the information by committing it to database
              user.save(using = self._db)
# return the user object
              return user
# To create a superuse account
       def create_superuser(self, email, profile_pic, password=None):
# create a user object which is manifested by the return of create_user method
              user = self.create_user(email, profile_pic , password)
# then we will conver the account to superuser by setting the following fields to True
              user.is_admin        = True
              user.is_active       = True
              user.is_staff        = True
              user.is_superadmin   = True

              print('create_superuser: ', user)
# Now save the configured fields in the user object
              user.save(using = self._db)
              return user
class UserAccount(AbstractBaseUser):
# set the basic fields for this account
       username     = models.CharField(max_length=50, unique=True)
       email         = models.EmailField(max_length=50, unique=True)
       profile_pic  = models.ImageField(blank=True, upload_to='userprofile/')
# fields to be filled by django
       date_created   = models.DateTimeField(auto_now=True)
       profile_updated = models.DateTimeField(auto_now=True)
       last_login     = models.DateTimeField(auto_now=True)
# fields to creae a superuse and to activate the account
       is_active     = models.BooleanField(default=False)
       is_staff      = models.BooleanField(default=False)
       is_superadmin = models.BooleanField(default=False)
       is_admin      = models.BooleanField(default=False)
# to set the emai to be used as the username
       USERNAME_FIELD = 'email'
# fields required to be filled
       #REQUIRED_FIELD = ['email']
# createing AccountManager object
       objects = AccountManager()
# own methods
       def __str__(self):
              return self.email

       def has_perm(self, perm, obj = None):
              return self.is_admin

       def has_module_perms(self, add_label):
              return True
         
    
