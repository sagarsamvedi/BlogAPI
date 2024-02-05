from rest_framework import serializers
from .models import Blog

class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        # Exclude the 'created_at' and 'updated_at' fields from serialization
        exclude = ['created_at', 'updated_at']
