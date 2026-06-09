from django.db import models
from Accounts.models import User

class Category(models.Model):
    category_name = models.CharField(max_length=255)
    description   = models.TextField()

class Course(models.Model):
    category    = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    user        = models.ForeignKey(User, on_delete=models.CASCADE)
    course_name = models.CharField(max_length=255)
    description = models.TextField()
    status      = models.CharField(max_length=50)
    created_at  = models.DateTimeField(auto_now_add=True)

class Chapter(models.Model):
    course     = models.ForeignKey(Course, on_delete=models.CASCADE)
    title      = models.CharField(max_length=255)
    content    = models.TextField()
    video_url  = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

class Enrollment(models.Model):
    user        = models.ForeignKey(User, on_delete=models.CASCADE)
    course      = models.ForeignKey(Course, on_delete=models.CASCADE)
    enroll_date = models.DateTimeField(auto_now_add=True)
    progress    = models.CharField(max_length=50)
    completion  = models.CharField(max_length=50)

class BrowseHistory(models.Model):
    user           = models.ForeignKey(User, on_delete=models.CASCADE)
    course         = models.ForeignKey(Course, on_delete=models.CASCADE)
    recently_opened = models.DateTimeField(auto_now = True)
    last_watched   = models.DateTimeField(null=True, blank=True)
    newly_added    = models.DateTimeField(auto_now_add=True)