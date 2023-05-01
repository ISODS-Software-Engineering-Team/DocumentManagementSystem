import mimetypes
import os

from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from Document.models import Document
from .models import Category, Competition
from Document.serialisers import DocumentSerializer, UserSerializer, UserLoginSerializer, CategorySerializer,CompetitionSerializer
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics
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
    
class CompetitionListCreateView(generics.ListCreateAPIView):
    queryset = Competition.objects.all()
    serializer_class = CompetitionSerializer
    
def get_all_competitions(request):
    competitions = list(Competition.objects.all().values())
    return JsonResponse(competitions, safe=False)

@api_view(['DELETE'])
def delete_competition(request, competition_id):
    try:
        competition = Competition.objects.get(id=competition_id)
    except Competition.DoesNotExist:
        return Response({'error': 'Competition does not exist.'}, status=status.HTTP_404_NOT_FOUND)

    competition.delete()
    return Response({'message': 'Competition deleted successfully.'}, status=status.HTTP_200_OK)

@api_view(['PUT'])
def update_competition(request, competition_id):
    try:
        competition = Competition.objects.get(id=competition_id)
    except Competition.DoesNotExist:
        return Response({'error': 'Competition does not exist.'}, status=status.HTTP_404_NOT_FOUND)

    serializer = CompetitionSerializer(competition, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Need to implement write_chunk method for larger file such as 1TB or so
# chunk_size = 1000
# # filesystem APIs
# def split():
#     def write_chunk(part, lines):
#         with open('../comp-data' + str(part) + '.csv', 'w') as f_out:
#             f_out.write(header)
#             f_out.writelines(lines)
#     with open('data.csv', 'r') as f:
#         count = 0
#         header = f.readLine()
#         lines = []
#         for line in f:
#             count += 1
#             lines.append(line)
#             if count % chunk_size == 0:
#                 write_chunk(count // chunk_size, line)
#                 lines = []
#         # write remainder
#         if len(lines) > 0:
#             write_chunk((count // chunk_size) + 1, lines)


""" 
    function for download a csv file
    define download function globally so multiple classes can use them.
    Need to change the file name corresponding with extension such as .csv
"""
def download_file(request):
    model = Competition
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    filename = 'LTC.csv'
    filepath = BASE_DIR + '/media/private_test/' + filename
    path = open(filepath, 'r')
    mime_type, _ = mimetypes.guess_type(filepath)
    response = HttpResponse(path, content_type=mime_type)
    response['Content-Disposition'] = "attachment; filename=%s" % filename
    return response


"""
    Class to download a file with specific competition id.
"""
class DownloadCompetition(ListAPIView):
    model = Competition
    serializer_class = CompetitionSerializer

    def get_queryset(self):
        return Competition.objects.all()

    def get(self, request, **kwargs):
        competition = get_object_or_404(Competition, id=kwargs.get('pk'))
        if competition.private_test_data.open("r"):
            return download_file(request)
        else:
            return HttpResponse("Not found")

