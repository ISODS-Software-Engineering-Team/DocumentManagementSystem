from rest_framework import serializers

from .models import Document, User, Category


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ('docs_id', 'category_id', 'brief', 'content', 'media_file', 'author',
                  'created_date', 'document_image')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password']
        extra_kwargs = {'password': {'write_only': True}}


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('category_id', 'category_name')
