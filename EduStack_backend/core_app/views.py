from django.shortcuts import render
from django.db.models import Q

from . import models, serializers

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination


# category create
@api_view(['GET', 'POST'])
def category_list_create(request):
    if request.method == 'GET':
        categories = models.Category.objects.all()
        serializer = serializers.CategorySerializers(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST': 
        if not request.user.is_authenticated or request.user.role != 'admin':
            return Response({'detail': "Only admin can create categories"}, status=status.HTTP_403_FORBIDDEN)
        else:
            serializer = serializers.CategorySerializers(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# course create
@api_view(['GET', 'POST'])
def course_list_create(request):
    if request.method == 'GET':
        category = request.query_params.get('category')
        search = request.query_params.get('search')

        queryset = models.Course.objects.all()

        if category:
            queryset = queryset.filter(category__title__icontains=category)

        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search)
            )

        if request.user.is_authenticated and request.user.role == 'teacher':
            queryset = queryset.filter(instructor=request.user)

        paginator = PageNumberPagination()
        paginator.page_size = 10
        paginated_queryset = paginator.paginate_queryset(queryset, request)

        serializer = serializers.CourseSerializers(
            paginated_queryset,
            many=True, 
            context={'request': request}
        )
        return paginator.get_paginated_response(serializer.data)

    elif request.method == 'POST':
        if not request.user.is_authenticated or request.user.role != 'teacher':
            return Response({'detail': 'Only teachers can create courses'}, status=status.HTTP_403_FORBIDDEN)

        data = request.data.copy()
        if 'instructor' not in data:
            data['instructor'] = request.user.id

        serializer = serializers.CourseSerializers(data=data)
        if serializer.is_valid():
            serializer.save(instructor=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# lesson create
@api_view(['GET', 'POST'])
def lesson_list_create(request):
    if request.method == 'GET':
        course = request.query_params.get('courseId')
        if not course:
            return Response({'detail': 'Course ID is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            course = models.Course.objects.get(pk=course)
        except models.Course.DoesNotExist:
            return Response({'detail': 'Course not found!!'}, status=status.HTTP_404_NOT_FOUND)

        is_teacher = request.user.is_authenticated and request.user.role == 'teacher' and request.user == course.instructor
        is_admin = request.user.is_authenticated and request.user.role == 'admin'
        if request.user.is_authenticated and request.user.role == 'student':
            is_enrolled = models.Enrollment.objects.filter(student=request.user, course=course, is_active=True).exists()
        else:
            is_enrolled = False

        if not (is_teacher or is_admin or is_enrolled):
            return Response({'detail': "You dont have permission to view this lesson"}, status=status.HTTP_403_FORBIDDEN)
        else:
            lessons = models.Lesson.objects.filter(course=course)
            serializer = serializers.LessonSerializers(lessons, many=True)
            return Response(serializer.data)

    elif request.method == 'POST':
        course_id = request.data.get('course') or request.query_params.get('courseId')
        if not course_id:
            return Response({'detail': 'Course ID is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            course = models.Course.objects.get(pk=course_id)
        except models.Course.DoesNotExist:
            return Response({'detail': 'Course not found!!'}, status=status.HTTP_404_NOT_FOUND)

        if request.user != course.instructor:
            return Response({'detail': 'You can only add lessons to your own courses'}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = serializers.LessonSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# material
@api_view(['GET', 'POST'])
def material_list_create(request):
    if request.method == 'GET':
        lesson_id = request.query_params.get('lessonId')
        if not lesson_id:
            return Response({'detail': 'lesson ID is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            lesson = models.Lesson.objects.get(pk=lesson_id)
        except models.Lesson.DoesNotExist:
            return Response({'detail': 'Lesson not found!!'}, status=status.HTTP_404_NOT_FOUND)

        course = lesson.course
        is_teacher = request.user.is_authenticated and request.user.role == 'teacher' and request.user == course.instructor
        is_admin = request.user.is_authenticated and request.user.role == 'admin'
        if request.user.is_authenticated and request.user.role == 'student':
            is_enrolled = models.Enrollment.objects.filter(student=request.user, course=course, is_active=True).exists()
        else:
            is_enrolled = False

        if not (is_teacher or is_admin or is_enrolled):
            return Response({'detail': "You dont have permission to view this material"}, status=status.HTTP_403_FORBIDDEN)
        else:
            materials = models.Material.objects.filter(course=course)
            serializer = serializers.MaterialSerializers(materials, many=True)
            return Response(serializer.data)

    elif request.method == 'POST':
        course_id = request.data.get('course') or request.query_params.get('courseId')
        if not course_id:
            return Response({'detail': 'Course ID is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            course = models.Course.objects.get(pk=course_id)
        except models.Course.DoesNotExist:
            return Response({'detail': 'Course not found!!'}, status=status.HTTP_404_NOT_FOUND)

        if request.user != course.instructor:
            return Response({'detail': 'You can only add lessons to your own courses'}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = serializers.MaterialSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# enrollment
@api_view(['GET'])
def enrollment_list(request):
    if not request.user.is_authenticated:
        return Response({'detail': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)

    if request.user.role == 'teacher':
        course = request.query_params.get('courseId')
        if not course:
            enrollments = models.Enrollment.objects.filter(course__instructor=request.user)
            serializer = serializers.EnrollmentSerializers(enrollments, many=True)
            return Response(serializer.data)
        try:
            course = models.Course.objects.get(pk=course)
        except models.Course.DoesNotExist:
            return Response({'detail': 'Course not found!!'}, status=status.HTTP_404_NOT_FOUND)
        
        if request.user != course.instructor:
            return Response({'detail': 'You can only view the enrollment of your own Course'}, status=status.HTTP_403_FORBIDDEN)
        else:
            enrollments = models.Enrollment.objects.filter(course=course)
            serializer = serializers.EnrollmentSerializers(enrollments, many=True)
            return Response(serializer.data)

    elif request.user.role == 'student':
        enrollments = models.Enrollment.objects.filter(student=request.user)
        serializer = serializers.EnrollmentSerializers(enrollments, many=True)
        return Response(serializer.data)

    elif request.user.role == 'admin':
        enrollments = models.Enrollment.objects.all()
        serializer = serializers.EnrollmentSerializers(enrollments, many=True)
        return Response(serializer.data)

    else:
        return Response({'detail': 'Unauthorized Login'}, status=status.HTTP_403_FORBIDDEN)


# enroll in a course
@api_view(['POST'])
def enroll_course(request):
    if not request.user.is_authenticated or request.user.role != 'student':
        return Response({'details': 'Only students can enroll'}, status=status.HTTP_403_FORBIDDEN)

    course = request.data.get('course')
    payment_method = request.data.get('payment_method', 'free')
    price = request.data.get('price')

    try:
        course = models.Course.objects.get(pk=course)
    except models.Course.DoesNotExist:
        return Response({'detail': 'Course not found....'}, status=status.HTTP_404_NOT_FOUND)

    if models.Enrollment.objects.filter(student=request.user, course=course).exists():
        return Response({'detail': 'You are Already enrolled'}, status=status.HTTP_400_BAD_REQUEST)

    if price is None:
        price = course.price

    enrollment = models.Enrollment.objects.create(
        student=request.user,
        course=course,
        price=price
    )
    serializer = serializers.EnrollmentSerializers(enrollment)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def course_detail(request, pk):
    try:
        course = models.Course.objects.get(pk=pk)
    except models.Course.DoesNotExist:
        return Response({'detail': 'Course not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = serializers.CourseSerializers(course, context={'request': request})
        return Response(serializer.data)

    elif request.method == 'PUT':
        if not request.user.is_authenticated or request.user != course.instructor:
            return Response({'detail': 'Only the course instructor can update this course'}, status=status.HTTP_403_FORBIDDEN)
        serializer = serializers.CourseSerializers(course, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        if not request.user.is_authenticated or request.user != course.instructor:
            return Response({'detail': 'Only the course instructor can delete this course'}, status=status.HTTP_403_FORBIDDEN)
        course.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'DELETE'])
def enrollment_detail(request, pk):
    try:
        enrollment = models.Enrollment.objects.get(pk=pk)
    except models.Enrollment.DoesNotExist:
        return Response({'detail': 'Enrollment not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = serializers.EnrollmentSerializers(enrollment)
        return Response(serializer.data)

    elif request.method == 'DELETE':
        if not request.user.is_authenticated or (request.user != enrollment.student and request.user.role != 'admin'):
            return Response({'detail': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)
        enrollment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'PUT', 'DELETE'])
def lesson_detail(request, pk):
    try:
        lesson = models.Lesson.objects.get(pk=pk)
    except models.Lesson.DoesNotExist:
        return Response({'detail': 'Lesson not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = serializers.LessonSerializers(lesson)
        return Response(serializer.data)

    elif request.method == 'PUT':
        if not request.user.is_authenticated or request.user != lesson.course.instructor:
            return Response({'detail': 'Only the course instructor can update this lesson'}, status=status.HTTP_403_FORBIDDEN)
        serializer = serializers.LessonSerializers(lesson, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        if not request.user.is_authenticated or request.user != lesson.course.instructor:
            return Response({'detail': 'Only the course instructor can delete this lesson'}, status=status.HTTP_403_FORBIDDEN)
        lesson.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def assignment_list(request):
    if request.method == 'GET':
        assignments = models.Assignment.objects.all()
        serializer = serializers.AssignmentSerializers(assignments, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        if not request.user.is_authenticated or request.user.role != 'teacher':
            return Response({'detail': 'Only teachers can create assignments'}, status=status.HTTP_403_FORBIDDEN)
        serializer = serializers.AssignmentSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def assignment_detail(request, pk):
    try:
        assignment = models.Assignment.objects.get(pk=pk)
    except models.Assignment.DoesNotExist:
        return Response({'detail': 'Assignment not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = serializers.AssignmentSerializers(assignment)
        return Response(serializer.data)

    elif request.method == 'PUT':
        if not request.user.is_authenticated or request.user != assignment.course.instructor:
            return Response({'detail': 'Only the course instructor can update this assignment'}, status=status.HTTP_403_FORBIDDEN)
        serializer = serializers.AssignmentSerializers(assignment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        if not request.user.is_authenticated or request.user != assignment.course.instructor:
            return Response({'detail': 'Only the course instructor can delete this assignment'}, status=status.HTTP_403_FORBIDDEN)
        assignment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def submission_list(request):
    if not request.user.is_authenticated:
        return Response({'detail': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)

    if request.method == 'GET':
        if request.user.role == 'student':
            submissions = models.Submission.objects.filter(student=request.user)
        elif request.user.role in ('teacher', 'admin'):
            submissions = models.Submission.objects.all()
        else:
            submissions = models.Submission.objects.none()
        serializer = serializers.SubmissionSerializers(submissions, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        if request.user.role != 'student':
            return Response({'detail': 'Only students can submit assignments'}, status=status.HTTP_403_FORBIDDEN)
        serializer = serializers.SubmissionSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save(student=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'DELETE'])
def submission_detail(request, pk):
    try:
        submission = models.Submission.objects.get(pk=pk)
    except models.Submission.DoesNotExist:
        return Response({'detail': 'Submission not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = serializers.SubmissionSerializers(submission)
        return Response(serializer.data)

    elif request.method == 'DELETE':
        if not request.user.is_authenticated or request.user != submission.student:
            return Response({'detail': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)
        submission.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def result_list(request):
    if not request.user.is_authenticated:
        return Response({'detail': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)

    if request.method == 'GET':
        if request.user.role == 'student':
            results = models.Result.objects.filter(student=request.user)
        elif request.user.role in ('teacher', 'admin'):
            results = models.Result.objects.all()
        else:
            results = models.Result.objects.none()
        serializer = serializers.ResultSerializers(results, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        if not request.user.is_authenticated or request.user.role not in ('teacher', 'admin'):
            return Response({'detail': 'Only teachers or admins can post results'}, status=status.HTTP_403_FORBIDDEN)
        serializer = serializers.ResultSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save(graded_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def result_detail(request, pk):
    try:
        result = models.Result.objects.get(pk=pk)
    except models.Result.DoesNotExist:
        return Response({'detail': 'Result not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = serializers.ResultSerializers(result)
        return Response(serializer.data)

    elif request.method == 'PUT':
        if not request.user.is_authenticated or request.user.role not in ('teacher', 'admin'):
            return Response({'detail': 'Only teachers or admins can update results'}, status=status.HTTP_403_FORBIDDEN)
        serializer = serializers.ResultSerializers(result, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        if not request.user.is_authenticated or request.user.role not in ('teacher', 'admin'):
            return Response({'detail': 'Only teachers or admins can delete results'}, status=status.HTTP_403_FORBIDDEN)
        result.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
