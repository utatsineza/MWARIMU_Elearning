from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema
from .models import Category, Course, Chapter, Enrollment, BrowseHistory
from Accounts.permissions import IsStudent, IsInstructor, IsInstructorOrAdmin
from .serializers import (CategorySerializer, CourseSerializer, ChapterSerializer,
                          EnrollmentSerializer, BrowseHistorySerializer)


class CategoryListView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        description="List all categories",
        responses={200: CategorySerializer(many=True)},
        tags=['Categories']
    )
    def get(self, request):
        categories = Category.objects.all()
        return Response(CategorySerializer(categories, many=True).data)

    @extend_schema(
        request=CategorySerializer,
        description="Create a new category",
        tags=['Categories']
    )
    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CourseListView(APIView):

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsInstructorOrAdmin()]
        return [IsAuthenticated()]

    @extend_schema(
        description="List all courses",
        responses={200: CourseSerializer(many=True)},
        tags=['Courses']
    )
    def get(self, request):
        courses = Course.objects.all()
        return Response(CourseSerializer(courses, many=True).data)

    @extend_schema(
        request=CourseSerializer,
        description="Create a new course (Instructor/Admin only)",
        tags=['Courses']
    )
    def post(self, request):
        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CourseDetailView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        description="Get course details",
        responses={200: CourseSerializer},
        tags=['Courses']
    )
    def get(self, request, course_id):
        try:
            course = Course.objects.get(course_id=course_id)
            return Response(CourseSerializer(course).data)
        except Course.DoesNotExist:
            return Response({'error': 'Course not found'}, status=status.HTTP_404_NOT_FOUND)

    @extend_schema(
        request=CourseSerializer,
        description="Update a course",
        tags=['Courses']
    )
    def put(self, request, course_id):
        try:
            course = Course.objects.get(course_id=course_id)
            serializer = CourseSerializer(course, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Course.DoesNotExist:
            return Response({'error': 'Course not found'}, status=status.HTTP_404_NOT_FOUND)

    @extend_schema(
        description="Delete a course",
        tags=['Courses']
    )
    def delete(self, request, course_id):
        try:
            course = Course.objects.get(course_id=course_id)
            course.delete()
            return Response({'message': 'Course deleted'}, status=status.HTTP_204_NO_CONTENT)
        except Course.DoesNotExist:
            return Response({'error': 'Course not found'}, status=status.HTTP_404_NOT_FOUND)


class ChapterListView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        description="List all chapters for a course",
        responses={200: ChapterSerializer(many=True)},
        tags=['Chapters']
    )
    def get(self, request, course_id):
        chapters = Chapter.objects.filter(course_id=course_id)
        return Response(ChapterSerializer(chapters, many=True).data)

    @extend_schema(
        request=ChapterSerializer,
        description="Add a chapter to a course",
        tags=['Chapters']
    )
    def post(self, request, course_id):
        serializer = ChapterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EnrollmentView(APIView):
    permission_classes = [IsStudent]

    @extend_schema(
        description="Get enrollments for a user",
        responses={200: EnrollmentSerializer(many=True)},
        tags=['Enrollment']
    )
    def get(self, request, user_id=None):
        enrollments = Enrollment.objects.filter(user_id=user_id)
        return Response(EnrollmentSerializer(enrollments, many=True).data)

    @extend_schema(
        request=EnrollmentSerializer,
        description="Enroll in a course",
        tags=['Enrollment']
    )
    def post(self, request, user_id=None):
        serializer = EnrollmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)