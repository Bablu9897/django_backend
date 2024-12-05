from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializers import UserSerializer, DataSerializer
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import *
from django.shortcuts import get_object_or_404

#  1. POST /api/sighnup
class SignupView(APIView):
    # Allow any user to access the signup endpoint
    permission_classes = [AllowAny]
   
    def post(self, request):
        """
        Handle POST requests for user signup.
        The data is validated using the UserSerializer and the password is hashed before saving.
        If the user is created successfully, return a success message with the user ID.
        """
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.validated_data['password'] = make_password(serializer.validated_data['password'])
                user = serializer.save()

            except Exception as e:
                return Response({"message": f"Error creating user: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return Response({"message": "User created successfully", "user_id":user.id }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#  2. POST /api/login
class LoginView(APIView):
     
    def post(self, request):
        """
        Handle POST requests for user login.
        The user is authenticated using email and password. 
        A JWT token is returned if the credentials are valid.
        If the user is not found or the credentials are incorrect, an error message is returned.
        """
        email = request.data.get('email')
        password = request.data.get('password')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
     
        if user.check_password(password):
            try:
                refresh = RefreshToken.for_user(user)
                return Response({
                    "message": "Login successful",
                    "token": str(refresh.access_token)
                })
            except Exception as e:
                return Response({"message": f"Error generating token: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response({"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)


# 3. GET /api/users (Admin only)
class UserListView(ListAPIView):
    """
    Retrieve a list of all users. Admin-only access.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]




class UserDetailAPI(APIView):
    permission_classes = [IsAuthenticated]

# 4. GET /api/users/<id>
    def get(self, request, id):
        """ 
        Retrieve a specific user's details by ID.
        If the user is not found, return a 404 error.
        """
        try:
            user = get_object_or_404(User, id=id)
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": f"Error retrieving user: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# 5. PUT /api/users/<id>

    def put(self, request, id):
        """
        Update a specific user's information by ID.
        If the user is not found, return a 404 error.
        """
        user = get_object_or_404(User, id=id)
        try:
            user = get_object_or_404(User, id=id)
            serializer = UserSerializer(user, data=request.data, partial=True)  # Allow partial updates
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "User updated successfully"}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message": f"Error updating user: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# 6. DELETE /api/users/<id>
    def delete(self, request, id):
        """
        Delete a specific user by ID.
        If the user is not found, return a 404 error.
        """
        try:
            user = get_object_or_404(User, id=id)
            user.delete()
            return Response({"message": "User deleted successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": f"Error deleting user: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DataAPI(APIView):
    # Only authenticated users can access the Data API
    permission_classes = [IsAuthenticated]

# 7. POST /api/data
    def post(self, request):
        """
        Create a record of Data.
        If the data is valid, save it and return the created data's title and description.
        """
        try:
            serializer = DataSerializer(data=request.data)
            if serializer.is_valid():
                data = serializer.save()
                return Response({
                        "title": data.title,
                        "description": data.description
                    }, status=status.HTTP_201_CREATED)
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            return Response({"message": f"Error creating data: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# 8. GET /api/data/<id>        
    def get(self, request, id):
        """
        Retrieve a specific data's details by ID.
        If the data is not found, return a 404 error.
        """
        try:
            data = get_object_or_404(Data, id=id)
            serializer = DataSerializer(data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({"message": f"Error retrieving data: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# 9. PUT /api/data/<id>    
    def put(self, request, id):
        """
        Handle PUT request to update Data.
        If only the title is updated, return a specific message.
        """
        try:
            if request.data.get('title', '') != "" and request.data.get('description', '') == "":
                msg = "Updated Title"
            else:
                msg = "Data updated successfully"
            
            data = get_object_or_404(Data, id=id)
            serializer = DataSerializer(data, data=request.data, partial=True)
            
            if serializer.is_valid():
                serializer.save()
                return Response({"message": msg}, status=status.HTTP_200_OK)
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            return Response({"message": f"Error updating data: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# 10. DELETE /api/data/<id>
    def delete(self, request, id):
        """
        Delete a specific data record by ID.
        If the data is not found, return a 404 error.
        """
        try:
            data = get_object_or_404(Data, id=id)
            data.delete()
            return Response({"title": "Data deleted successfully"}, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({"message": f"Error deleting data: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)