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
        paginated_queryset = paginator.paginate_queryset(queryset, request)




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
    ''



