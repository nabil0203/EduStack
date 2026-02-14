from django.db import models

from django.contrib.auth.models import AbstractUser



USER_ROLES = (
    ('admin', 'Admin'),
    ('teacher', 'Teacher'),
    ('student', 'Student')
)



class User(AbstractUser):                                                             # 'AbstractUser' used to add extra features in the Django built-in 'User' class
    role = models.CharField(max_length=100, choices=USER_ROLES)                       # extra with the User class
    mobile_no = models.CharField(max_length=15)                                      # extra with the User class


    def __str__(self):
        return f"{self.id}. {self.username} - {self.role}"





