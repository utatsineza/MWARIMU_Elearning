from rest_framework import serializers
from .models import Category, Course, Chapter, Enrollment, BrowseHistory

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'

class ChapterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chapter
        fields = '__all__'

class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = '__all__'

class BrowseHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BrowseHistory
        fields = '__all__'