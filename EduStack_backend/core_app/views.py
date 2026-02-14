from django.shortcuts import render

from . import models, serializers

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination

from django.db.models import Q





# category create
@api_view(['GET', 'POST'])
def category_list_create(request):

    if request.method == 'GET':

        categories = models.Category.objects.all()                                          # getting all objects as query set/dictionary
        serializer = serializers.CategorySerializers(categories, many = True)               # converting the dictionaries into JSON using serializers

        return Response(serializer.data, status=status.HTTP_200_OK)



    elif request.method == 'POST': 

        if not request.user.is_authenticated or request.user.role != 'admin':                       # user = not authenticated / not admin
            return Response({'detail' : "Only admin can create categories"})                        # can not create any category


        else:                                                                                       # user = authenticated / admin
            serializer = serializers.CategorySerializers(data = request.data)                       # sending the data by serializer as JSON
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            

            










# category create
@api_view(['GET', 'POST'])
def course_list_create(request):

    # Course will be shown Category-wise
    # 1 category has multiple course
    if request.method == 'GET':

        category = request.query_params.get('category')                             # Query Parameters -> Key-value pairs; getting a category
        search = request.query_params.get('search')                                 # Query Parameters

        queryset = models.Course.objects.all()


        if category:                                                                   # if category exists and user wants to filter based on category
            queryset = queryset.filter(category__title__icontains = category)

        if search:                                                                     # search  
            queryset = queryset.filter(
                Q(title__icontains = search) |
                Q(description__icontains = search)
            )


        
        if request.user.is_authenticated and request.user.role == 'teacher':
            queryset = queryset.filter(instructor = request.user)                               # teacher can only see his own created courses



        paginator = PageNumberPagination()
        paginator.page_size = 10
        paginated_queryset = paginator.paginate_queryset(queryset, request)                      # pagination must work in both search and category



        serializer = serializers.CourseSerializers(
            paginated_queryset,
            many = True, 
            context = {'request' : request}
        )



        return paginator.get_paginated_response(serializer.data)
    





    elif request.method == 'POST':
        if not request.user.is_authenticated or request.user.role != 'teacher':                                  # if not only teachers
            return Response({'detail' : {'Only teachers can create courses'}})

        else:
            serializer = serializers.CategorySerializers(data = request.data)

            if serializers.is_valid():
                serializers.save()
                return Response (serializer.data, status=status.HTTP_201_CREATED)
            
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)














@api_view(['GET', 'POST'])
def lesson_list_create(request):

    # get
    if request.method == 'GET':
        course = request.query_params.get('courseId')

        if not course:
            return Response({'detail' : 'Course ID is required'})                     # in url --> "?course = python" or "?courseId=1"; all the lessons of the python course will be shown
        
        try:
            course = models.Course.objects.get(pk = course)
        except models.Course.DoesNotExist:
            return Response({'detail' : 'Course nor found!!'})                        # invalid course ID


        # user is a teacher or not
        is_teacher = request.user.is_authenticated and request.user.role == 'teacher' and request.user == course.instructor

        # user is an admin or not
        is_admin = request.user.is_authenticated and request.user.role == 'admin'


        # identify if the student is enrolled in a course or not
        if request.user.is_authenticated and request.user.role == 'student':
            is_enrolled = models.Enrollment.objects.filter(student = request.user, course = course, status = 'active').exists()                   # returns true if the student is enrolled 
        else:
            is_enrolled = False


        if not (is_teacher or is_admin or is_enrolled):                                                                 # user is logged in but not teacher/admin/enrolled
            return Response({'detail' : "You dont have permission to view this lesson"})                                # can't view the lesson
        
        else:
            lessons = models.Lesson.objects.filter(course=course)

            serializer = serializers.LessonSerializers(lessons, many = True)
            return Response(serializer.data)
    



    # POST
    elif request.method == 'POST':
        course = request.query_params.get('courseId')

        if not course:
            return Response({'detail' : 'Course ID is required'})                     # in url --> "?course = python" or "?courseId=1"; all the lessons of the python course will be shown
        
        try:
            course = models.Course.objects.get(pk = course)
        except models.Course.DoesNotExist:
            return Response({'detail' : 'Course nor found!!'})                        # invalid course ID



        # only the course instructor add lesson to the course
        if request.user != course.instructor:
            return Response({'detail' : 'You can only add lessons to your own courses'})
        
        else:
            serializer = serializers.LessonSerializers(data = request.data)

            if serializers.is_valid():
                serializers.save()
                return Response (serializer.data, status=status.HTTP_201_CREATED)
            
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


        




    
    


# material
# same as lesson
@api_view(['GET', 'POST'])
def material_list_create(request):

    # get
    if request.method == 'GET':
        lesson = request.query_params.get('lessonId')

        if not lesson:
            return Response({'detail' : 'lesson ID is required'})                     # in url --> "?lesson = python" or "?courseId=1"; all the lessons of the python course will be shown
        
        try:
            lesson = models.Lesson.objects.get(pk = lesson)
        except models.Lesson.DoesNotExist:
            return Response({'detail' : 'Lesson nor found!!'})                        # invalid lesson ID


        #to identify which course
        course = lesson.course


        # user is a teacher or not
        is_teacher = request.user.is_authenticated and request.user.role == 'teacher' and request.user == course.instructor

        # user is an admin or not
        is_admin = request.user.is_authenticated and request.user.role == 'admin'


        # identify if the student is enrolled in a course or not
        if request.user.is_authenticated and request.user.role == 'student':
            is_enrolled = models.Enrollment.objects.filter(student = request.user, course = course, status = 'active').exists()                   # returns true if the student is enrolled 
        else:
            is_enrolled = False


        if not (is_teacher or is_admin or is_enrolled):                                                                   # user is logged in but not teacher/admin/enrolled
            return Response({'detail' : "You dont have permission to view this material"})                                # can't view the material
        
        else:
            materials = models.Material.objects.filter(course=course)

            serializer = serializers.MaterialSerializers(materials, many = True)
            return Response(serializer.data)
    



    # POST
    elif request.method == 'POST':
        course = request.query_params.get('courseId')

        if not course:
            return Response({'detail' : 'Course ID is required'})

        try:
            course = models.Course.objects.get(pk = course)
        except models.Course.DoesNotExist:
            return Response({'detail' : 'Course nor found!!'})                        # invalid course ID



        # only the course instructor add lesson to the course
        if request.user != course.instructor:
            return Response({'detail' : 'You can only add lessons to your own courses'})
        
        else:
            serializer = serializers.LessonSerializers(data = request.data)

            if serializers.is_valid():
                serializers.save()
                return Response (serializer.data, status=status.HTTP_201_CREATED)
            
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
   


    






# enrollment
# only get request
@api_view(['GET', 'POST'])
def enrollment_list(request):

    if request.method == 'GET':

        if request.user.role == 'teacher':
            course = request.query_params('courseId')

            if not course:
                return Response({'detail' : 'Course ID is required'})
            try:
                course = models.Course.objects.get(pk = course)
            except models.Course.DoesNotExist:
                return Response({'detail' : 'Course nor found!!'})
            

            if request.user != course.instructor:                                                            # if not the course instructor, he can't see the enrollment
                return Response({'detail' : 'You can only view the enrollment of your own Course'})

            else:
                enrollments = models.Enrollment.objects.filter(course = course)
                serializer = serializers.EnrollmentSerializers(enrollments, many = True)
                return Response(serializer.data)
        

        elif request.user.role == 'student':                                                                # student can only see his enrolled courses
            enrollments = models.Enrollment.objects.filter(student = request.user)
            serializer = serializers.EnrollmentSerializers(enrollments, many = True)
            return Response(serializer.data)
        


        elif request.user.role == 'admin':
            return Response({'detail' : 'Go to admin dashboard'})
        

        else:
            return Response({'detail' : 'Unauthorized Login'})










# enroll in a course

@api_view(['POST'])
def enroll_course(request):
    
    if request.user.role != 'student':                                                  # if anyone tries to enroll who is not student
        return Response({'details' : 'Only students can enroll'})


    course = request.data.get('course')                                                 # if student
    payment_method = request.data.get('payment_method', 'free')
    price = request.data.get('price')


    try:
        course = models.Course.objects.get(pk = course)
    except models.Course.DoesNotExist:
        return Response({'detail' : 'Course not found....'})
    


    if models.Enrollment.objects.filter(student = request.user, course = course).exists():                             # if the student is already exists
        return Response({'detail' : 'You are Already enrolled'})


    enrollment = models.Enrollment.objects.create(                                          # make new enrollment
        student = request.user,
        course = course,
        price = price
    )

    serializer = serializers.EnrollmentSerializers(enrollment)

    return Response(serializer.data, status=status.HTTP_201_CREATED)



   

