from rest_framework import serializers
from .models import User, Data
from django.core.exceptions import ValidationError

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer to handle User creation, validation, and updates.
    Password is marked as write-only for security reasons.
    """
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}  # Ensure password is not returned in responses
        }
    


class DataSerializer(serializers.ModelSerializer):
    """
    Serializer for handling Data creation, retrieval, and updates.
    """
    
    class Meta:
        model = Data
        fields = ['id', 'title', 'description']
    
    def validate_title(self, value):
        """
        Custom validation for the title to ensure it's not empty.
        """
        if not value.strip():
            raise serializers.ValidationError("Title cannot be empty.")
        return value

    def validate_description(self, value):
        """
        Custom validation for the description to ensure it's not empty.
        """
        if not value.strip():
            raise serializers.ValidationError("Description cannot be empty.")
        return value
