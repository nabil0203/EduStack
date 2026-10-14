from django.shortcuts import render
from django.contrib.auth import authenticate

from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from users_app.models import User
from .serializers import UserSerializer, UserRegistrationSerializer


@api_view(['GET', 'POST'])
def user_list_create(request):
    if not request.user.is_authenticated:
        return Response({'detail': 'Authentication Credentials is not provided'}, status=status.HTTP_401_UNAUTHORIZED)
        
    if request.method == 'GET':
        if request.user.role == 'admin':
            users = User.objects.all()
        else:
            users = User.objects.filter(id=request.user.id)
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        if request.user.role == 'admin':
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.save()
                if 'password' in serializer.validated_data:
                    user.set_password(serializer.validated_data['password'])
                    user.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'detail': 'You do not have this power'}, status=status.HTTP_403_FORBIDDEN)


# Register View (renders the HTML form in DRF browsable API)
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save(role='student')
        user.set_password(serializer.validated_data['password'])
        user.save()
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            'message': 'User registered successfully',
            'token': token.key,
            'user': UserSerializer(user).data
        }, status=status.HTTP_201_CREATED)

register_user = RegisterView.as_view()


# Login View
@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    username = request.data.get('username')
    password = request.data.get('password')
    if not username or not password:
        return Response({'detail': 'Username and password are required'}, status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(username=username, password=password)
    if not user:
        return Response({'detail': 'Invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED)

    token, _ = Token.objects.get_or_create(user=user)
    return Response({
        'token': token.key,
        'user': UserSerializer(user).data
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def protected_view(request):
    return Response({
        'message': f'Hello {request.user.username}, you are authenticated!',
        'role': request.user.role
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
def teacher_list(request):
    teachers = User.objects.filter(role='teacher')
    serializer = UserSerializer(teachers, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def teacher_detail(request, pk):
    try:
        teacher = User.objects.get(pk=pk, role='teacher')
    except User.DoesNotExist:
        return Response({'detail': 'Teacher not found'}, status=status.HTTP_404_NOT_FOUND)
    serializer = UserSerializer(teacher)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def student_list(request):
    students = User.objects.filter(role='student')
    serializer = UserSerializer(students, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def student_detail(request, pk):
    try:
        student = User.objects.get(pk=pk, role='student')
    except User.DoesNotExist:
        return Response({'detail': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)
    serializer = UserSerializer(student)
    return Response(serializer.data, status=status.HTTP_200_OK)
