from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse, FileResponse
from django.shortcuts import get_object_or_404
import mimetypes
import os
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.http import HttpResponse
from Document.models import Document
from .models import Category, Competition
from Document.serialisers import DocumentSerializer, UserSerializer, UserLoginSerializer, CategorySerializer, CompetitionSerializer
from rest_framework.decorators import api_view


class CreateCategory(ListCreateAPIView):
    model = Category
    serializer_class = CategorySerializer

    def get_queryset(self):
        return Category.objects.all()

    def create_category(self, request, *args, **kwargs):

        serializer = CategorySerializer()
        if serializer.is_valid():
            serializer.save()

            return JsonResponse(serializer.data)({
                'message': 'Create a new Category successful!'
            }, status=status.HTTP_201_CREATED)

        return JsonResponse({
            'message': 'Create a new Document unsuccessful!'
        }, status=status.HTTP_400_BAD_REQUEST)

class ListCreateDocumentView(ListCreateAPIView):
    model = Document
    serializer_class = DocumentSerializer

    def get_queryset(self):
        return Document.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = DocumentSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return JsonResponse({
                'message': 'Create a new Document successful!'
            }, status=status.HTTP_201_CREATED)

        return JsonResponse({
            'message': 'Create a new Document unsuccessful!'
        }, status=status.HTTP_400_BAD_REQUEST)


class UpdateDeleteDocumentView(RetrieveUpdateDestroyAPIView):
    model = Document
    serializer_class = DocumentSerializer

    def put(self, request, *args, **kwargs):
        document = get_object_or_404(Document, id=kwargs.get('pk'))
        serializer = DocumentSerializer(post, data=request.data)

        if serializer.is_valid():
            serializer.save()

            return JsonResponse({
                'message': 'Update Document successful!'
            }, status=status.HTTP_200_OK)

        return JsonResponse({
            'message': 'Update Document unsuccessful!'
        }, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        document = get_object_or_404(Document, id=kwargs.get('pk'))
        document.delete()

        return JsonResponse({
            'message': 'Delete Document successful!'
        }, status=status.HTTP_200_OK)


class UserRegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['password'] = make_password(serializer.validated_data['password'])
            serializer.save()

            return JsonResponse({
                'message': 'Register successful!'
            }, status=status.HTTP_201_CREATED)

        else:
            return JsonResponse({
                'error_message': 'This email has already exist!',
                'errors_code': 400,
            }, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(
                request,
                username=serializer.validated_data['email'],
                password=serializer.validated_data['password']
            )
            if user:
                refresh = TokenObtainPairSerializer.get_token(user)
                data = {
                    'refresh_token': str(refresh),
                    'access_token': str(refresh.access_token)
                }
                return Response(data, status=status.HTTP_200_OK)

            return Response({
                'error_message': 'Email or password is incorrect!',
                'error_code': 400
            }, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            'error_messages': serializer.errors,
            'error_code': 400
        }, status=status.HTTP_400_BAD_REQUEST)


class DeleteCategoryView(RetrieveUpdateDestroyAPIView):
    model = Category
    serializer_class = CategorySerializer

    def get_queryset(self):
        return Category.objects.all()

    def delete(self, request, **kwargs):
        category = get_object_or_404(Category, id=kwargs.get('pk'))
        if category.delete():
            return JsonResponse({
                'message': 'Deleted Category Successful!'
            }, status=status.HTTP_200_OK)
        else:

            return JsonResponse({
                'message': 'Deleted Category unsuccessful!'
            }, status=status.HTTP_400_BAD_REQUEST)

class UpdateCategoryView(RetrieveUpdateDestroyAPIView):
    model = Document
    serializer_class = DocumentSerializer

    def get_queryset(self):
        return Document.objects.all()

    def put(self, request, **kwargs):
        category = get_object_or_404(Document, id=kwargs.get('pk'))
        serializer = DocumentSerializer(Document, data=request.data)

        if serializer.is_valid():
            serializer.save()

            return JsonResponse({
                'message': 'Update Category successful!'
            }, status=status.HTTP_200_OK)

        return JsonResponse({
            'message': 'Update Category unsuccessful!'
        }, status=status.HTTP_400_BAD_REQUEST)

"""
    Rewrite: LongNguyen
    Requirement:
    1. Create Competition.
    2. Read Competition: Display all Competitions in database, Display a specific Competition with id.
    3. Update Competition: Update a specific Competition with id.
    4. Delete Competition: Delete a specific competition with id.
"""

# Create Competition & Display all Competitions
class CompetitionAPIView(ListCreateAPIView):
    model = Competition
    serializer_class = CompetitionSerializer

    def get_queryset(self):
        return Competition.objects.all()

    def get_competition(self):
        queryset = self.get_queryset()
        return get_object_or_404(queryset)

    def create(self, request, *args, **kwargs):
        serializer = CompetitionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({
                'message': 'Created Competition successfully'
            }, status=status.HTTP_201_CREATED)
        else:
            return JsonResponse({
                'message': 'Created Competition unsuccessfully'
            }, status=status.HTTP_400_BAD_REQUEST)

# Display a specific Competition.
class SpecificCompetitionAPIView(ListAPIView):
    model = Competition
    serializer_class = CompetitionSerializer

    # override the get_queryset method to filter only the pk (primary key)
    # usually pk is the ID
    def get_queryset(self):
        return Competition.objects.filter(id=self.kwargs.get('pk'))

    # Call the get_queryset function and return it.
    def get_object(self):
        queryset = self.get_queryset()
        return get_object_or_404(queryset)


class UpdateAndDeleteCompetitionAPIView(RetrieveUpdateDestroyAPIView):
    model = Competition
    serializer_class = CompetitionSerializer

    def get_queryset(self):
        return Competition.objects.filter(id=self.kwargs.get('pk')).first()

    def delete(self, request, *args, **kwargs):
        # Try to get the object with specify id first
        try:
            competition = self.get_queryset()

            # if able to find the object
            if get_object_or_404(competition):
                # delete the object and return a message
                competition.delete()
                return JsonResponse({
                    'message': 'Deleted Competition Successfully'
                }, status=status.HTTP_200_OK)
            # catch exception
            # appearing exception is unreachable.
        except Competition.DoesNotExist:
            return JsonResponse({
                'message': 'Competition does not exist!'
            }, status=status.HTTP_404_NOT_FOUND)

    # Similar for delete logic.
    def update(self, request, *args, **kwargs):
        try:
            competition = self.get_queryset()
        except Competition.DoesNotExist:
            return JsonResponse({
                'message': 'Competition does not exist!'
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = CompetitionSerializer(competition, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
