from django.db import models
from Accounts.models import User

class Category(models.Model):
    category_name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.category_name

class Course(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='courses')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='courses', help_text="The Instructor who created the course")
    course_name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    course_type = models.CharField(max_length=50, help_text="'free', 'paid'")
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="nullable for free courses")
    status = models.CharField(max_length=50, help_text="'draft', 'under_review', 'published'")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.course_name

class Chapter(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='chapters')
    title = models.CharField(max_length=255)
    content = models.TextField(null=True, blank=True)
    chapter_type = models.CharField(max_length=50, help_text="'video', 'document', 'exercise'")
    video_url = models.URLField(max_length=500, null=True, blank=True)
    document_url = models.URLField(max_length=500, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Exercise(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name='exercises')
    question_text = models.TextField()
    correct_answer = models.TextField()

    def __str__(self):
        return f"Exercise for {self.chapter.title}"

class Enrollment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    enroll_date = models.DateTimeField(auto_now_add=True)
    progress = models.CharField(max_length=100, null=True, blank=True)
    completion = models.CharField(max_length=100, null=True, blank=True)
    access_status = models.CharField(max_length=50, help_text="'active', 'pending_payment', 'revoked'")

    def __str__(self):
        return f"{self.user.username} enrolled in {self.course.course_name}"

class StudentAnswer(models.Model):
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE, related_name='student_answers')
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE, related_name='student_answers')
    given_answer = models.TextField()
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"Answer by {self.enrollment.user.username} for {self.exercise.id}"

class BrowseHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='browse_histories')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='browse_histories')
    recently_opened = models.DateTimeField(auto_now=True)
    last_watched = models.DateTimeField(null=True, blank=True)
    newly_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"History for {self.user.username} - {self.course.course_name}"
