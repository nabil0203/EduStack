from django.db import models

from django.contrib.auth.models import AbstractUser



USER_ROLES = (
    ('admin', 'Admin'),
    ('teacher', 'Teachers'),
    ('student', 'Students')
)



class User(AbstractUser):                                         # 'AbstractUser' used to add extra features in the Django built-in 'User' class
    role = models.CharField(max_length=100)                       # extra with the User class
    mobile_no = models.CharField(max_length=100)                  # extra with the User class





