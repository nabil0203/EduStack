from django.db import models

from users_app.models import User                                              # taking users from the users_app; not the built-in django user model

# Create your models here.


class Category(models.Model):
    title = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        verbose_name_plural = "Categories" 

    def __str__(self):
        return self.title
    



class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    banner = models.ImageField(upload_to='media/course_banners/')
    price = models.FloatField()
    duration = models.FloatField()
    is_active = models.BooleanField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    instructor = models.ForeignKey(User, on_delete=models.CASCADE)                       # the User of users_app model
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    




class Lesson(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    video = models.FileField(upload_to='media/lessons_videos/')
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.title
    





class Material(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    file_type = models.CharField(max_length=100)
    file = models.FileField(upload_to='media/materials/')
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    








class Enrollment(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    price = models.FloatField()
    progress = models.IntegerField(default=0)
    is_completed = models.BooleanField(default=False)
    total_mark = models.FloatField(default=0)
    is_certificate_ready = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"{self.student.username} - {self.course.title}"                      # returns the specific username, title
    







class QuestionAnswer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



    def __str__(self):
        return f"{self.user_id.username} --> {self.lesson_id.title}"                         # returns the specific username and title of the question


class Assignment(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, null=True, blank=True)
    due_date = models.DateTimeField(null=True, blank=True)
    total_marks = models.FloatField(default=100)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.course.title}"


class Submission(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='media/submissions/', null=True, blank=True)
    text = models.TextField(blank=True, default='')
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.username} - {self.assignment.title}"


class Result(models.Model):
    submission = models.OneToOneField(Submission, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    marks_obtained = models.FloatField()
    feedback = models.TextField(blank=True, default='')
    graded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='graded_results')
    graded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.username} - {self.marks_obtained}"
