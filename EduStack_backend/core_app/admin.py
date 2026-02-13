from django.contrib import admin

from . import models

# Register your models here.


admin.site.register(models.Category)
admin.site.register(models.Course)
admin.site.register(models.Enrollment)
admin.site.register(models.Lesson)
admin.site.register(models.Material)
admin.site.register(models.QuestionAnswer)
