from rest_framework import serializers

from Document.models import Document, User, Category, Competition


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ('__all__')

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

class CompetitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Competition
        fields = ('__all__')
        # call __all__() method for all fields instead of writing everything.
