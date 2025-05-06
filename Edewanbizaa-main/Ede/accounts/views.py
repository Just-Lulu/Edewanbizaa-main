from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from django.contrib.auth import login, logout
from .serializers import CustomUserSerializer, CustomUserCreateSerializer, CustomUserUpdateSerializer
from .models import CustomUser

class UserRegistrationView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = CustomUserCreateSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            login(request, user)
            return Response({
                'user': CustomUserSerializer(user).data,
                'message': 'Registration successful'
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        try:
            user = CustomUser.objects.get(username=username)
            if user.check_password(password):
                login(request, user)
                return Response({
                    'user': CustomUserSerializer(user).data,
                    'message': 'Login successful'
                })
            return Response({'error': 'Invalid password'}, status=status.HTTP_400_BAD_REQUEST)
        except CustomUser.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

class UserLogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({'message': 'Logout successful'})

class UserProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CustomUserUpdateSerializer

    def get_object(self):
        return self.request.user

    def get(self, request, *args, **kwargs):
        serializer = CustomUserSerializer(request.user)
        return Response(serializer.data)
