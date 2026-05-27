from django.urls import path
from .views import (CategoryListView, CourseListView, CourseDetailView,
                    ChapterListView, EnrollmentView)

urlpatterns = [
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('courses/', CourseListView.as_view(), name='course-list'),
    path('courses/<int:course_id>/', CourseDetailView.as_view(), name='course-detail'),
    path('courses/<int:course_id>/chapters/', ChapterListView.as_view(), name='chapter-list'),
    path('enroll/', EnrollmentView.as_view(), name='enroll'),
    path('enroll/<int:user_id>/', EnrollmentView.as_view(), name='user-enrollments'),
]