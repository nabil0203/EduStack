from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response

from users_app.models import User                           # customized user 

from . serializers import UserSerializer



@api_view(['GET', 'POST'])
def user_list_create(request):


    # user is not authenticated
    if not request.user.is_authenticated:
        return Response({'detail' : 'Authentication Credentials is not provided'}, status=401)
        
    
    # user is authenticated
    if request.method == 'GET':                                                     # get request


        # if the user is admin ---> can view all the users
        if request.user.role == 'admin':
            users = User.objects.all()

        # if the user is not admin ---> can view only his details not all data
        else:
            users = User.objects.filter(id=request.user.id)


        serializer = UserSerializer(users, many = True)

        return Response(serializer.data)
    



    # user is authenticated
    elif request.method == 'POST':                                                   # POST request
         
        if request.user.role == 'admin':                                             # only admin can create POST request/add new data
            serializer = UserSerializer(data=request.data)  

            if serializer.is_valid():
               serializer.save()
               return Response(serializer.data, status=201)

            else:
                return Response(serializer.errors, status=400)
            

        else:
            return Response({'detail' : 'You do not have this power'}, status=401)
            

        









