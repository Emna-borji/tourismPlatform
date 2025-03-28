from django.http import JsonResponse
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from .models import CustomUser
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from .serializers import LoginSerializer
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from .serializers import UpdateProfileSerializer
from .serializers import ChangePasswordSerializer
from rest_framework import viewsets
from rest_framework.decorators import action





from .serializers import CustomUserSerializer
from rest_framework.permissions import BasePermission
from .permissions import IsAdmin  # Import the custom permission

class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated, IsAdmin]  # Apply custom IsAdmin permission

    def create(self, request, *args, **kwargs):
        # Prevent admins from creating users
        return Response({'error': 'Admins cannot create users.'}, status=status.HTTP_403_FORBIDDEN)

    def update(self, request, *args, **kwargs):
        # Prevent admins from updating users
        return Response({'error': 'Admins cannot update users.'}, status=status.HTTP_403_FORBIDDEN)

    def destroy(self, request, *args, **kwargs):
        # Ensure admins can only delete other users, not themselves
        if request.user.id == kwargs['pk']:
            return Response({'error': 'Admins cannot delete their own profile.'}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)

    @action(detail=True, methods=["post"], permission_classes=[IsAdmin])
    def block_user(self, request, pk=None):
        
        """Admin can block a user with start and end dates."""

        print("Received pk:", pk)  # Debugging line
        print(request.user)  # Debugging line
        print(request.user.role)
        user = CustomUser.objects.get(id=pk)  # Directly fetch the user
        print("Manually fetched user:", user)
        print(user)
        print(request.user.role)
        if request.user.role != "admin":
            return Response({"error": "Only admins can block users."}, status=status.HTTP_403_FORBIDDEN)
        

        if user.role == "admin":
            return Response({"error": "Admins cannot block other admins."}, status=status.HTTP_403_FORBIDDEN)

        start_date = request.data.get("blockstartdate")
        end_date = request.data.get("blockenddate")

        if start_date and end_date:
            # Block the user
            user.block_user(start_date, end_date)
            return Response(
                {"message": f"User {user.email} has been blocked from {start_date} to {end_date}."},
                status=status.HTTP_200_OK
            )
        else:
            # Unblock the user by setting the dates to None
            user.block_user(None, None)
            return Response({"message": f"User {user.email} has been unblocked."}, status=status.HTTP_200_OK)

        




@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    if request.method == 'POST':
        # Use the serializer to validate the data
        serializer = CustomUserSerializer(data=request.data)

        if serializer.is_valid():
            # Save the user and return a response
            serializer.save()
            return JsonResponse({"message": "User registered successfully!"}, status=201)

        # If validation fails, return error messages
        return JsonResponse({"error": serializer.errors}, status=400)

    return JsonResponse({"error": "Invalid method. Use POST."}, status=405)




@api_view(['POST'])
@permission_classes([AllowAny])  # Allow unauthenticated access to login
def login(request):
    # Your existing login logic
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']

        # Generate JWT tokens (access and refresh)
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        return Response({
            'access_token': access_token,
            'refresh_token': str(refresh),
        }, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_profile(request):
    user = request.user
    serializer = UpdateProfileSerializer(user, data=request.data, partial=True)
    
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    user = request.user
    serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
    
    if serializer.is_valid():
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        return Response({'message': 'Password changed successfully'})
    return Response(serializer.errors, status=400)







@api_view(['GET'])
@permission_classes([IsAuthenticated])  # Ensure that only authenticated users can view their profile
def view_profile(request):
    try:
        # Get the current user based on the request
        user = request.user

        # Serialize the user's data
        serializer = CustomUserSerializer(user)

        return Response(serializer.data, status=status.HTTP_200_OK)

    except CustomUser.DoesNotExist:
        return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
    


@api_view(['POST'])
def logout(request):
    # Since JWT is stateless, there is no need to "delete" or invalidate the token server-side.
    # You can choose to give a response that confirms the logout.
    
    response = Response({'message': 'Successfully logged out'})
    # You can also clear any session-related data or cookies if you're using them for the frontend.

    # If you're using cookies, you can also invalidate the JWT cookie like this:
    # response.delete_cookie('access_token')   # If JWT is stored in a cookie
    
    return response




