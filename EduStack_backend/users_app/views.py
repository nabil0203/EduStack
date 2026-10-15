from django.shortcuts import render
from django.contrib.auth import authenticate

from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

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


# Register View
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
        refresh = RefreshToken.for_user(user)
        return Response({
            'message': 'User registered successfully',
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': UserSerializer(user).data
        }, status=status.HTTP_201_CREATED)

register_user = RegisterView.as_view()


# Login View
@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    identifier = request.data.get('username') or request.data.get('phone')
    password = request.data.get('password')
    if not identifier or not password:
        return Response(
            {'detail': 'Username or phone and password are required'},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Look up user by username or phone number to get the actual username for authenticate()
    user_record = User.objects.filter(username=identifier).first()
    if user_record is None:
        user_record = User.objects.filter(mobile_no=identifier).first()

    user = authenticate(
        username=user_record.username if user_record else identifier,
        password=password
    )
    if not user:
        return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

    refresh = RefreshToken.for_user(user)
    return Response({
        'access': str(refresh.access_token),
        'refresh': str(refresh),
        'user': UserSerializer(user).data
    }, status=status.HTTP_200_OK)


# Logout View — blacklists the refresh token so it can't be reused
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_user(request):
    refresh_token = request.data.get('refresh')
    if not refresh_token:
        return Response({'detail': 'Refresh token is required'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)
    except TokenError:
        return Response({'detail': 'Invalid or expired token'}, status=status.HTTP_400_BAD_REQUEST)


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