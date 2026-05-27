from django.contrib import admin
from .models import Category, Course, Chapter, Enrollment, BrowseHistory

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display  = ['category_name', 'description']
    search_fields = ['category_name']

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display  = ['course_name', 'category', 'user', 'status', 'created_at']
    search_fields = ['course_name']
    list_filter   = ['status', 'category']

@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    list_display  = ['title', 'course', 'created_at']
    search_fields = ['title']

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display  = ['user', 'course', 'enroll_date', 'progress', 'completion']
    search_fields = ['user__email', 'course__course_name']

@admin.register(BrowseHistory)
class BrowseHistoryAdmin(admin.ModelAdmin):
    list_display  = ['user', 'course', 'recently_opened', 'last_watched']