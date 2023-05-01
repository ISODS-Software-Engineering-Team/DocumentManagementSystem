from django.urls import path

from . import views
from .views import UserRegisterView, UserLoginView

urlpatterns = [
    path('register', UserRegisterView.as_view(), name='register'),
    path('login', UserLoginView.as_view(), name='login'),
    path('documents', views.ListCreateDocumentView.as_view()),
    path('documents/<int:pk>', views.UpdateDeleteDocumentView.as_view()),
    path('category/<int:pk>', views.DeleteCategoryView.as_view()),
    path('update/<int:pk>/', views.UpdateCategoryView.as_view(), name='update-category'),
    path('competitions/', views.CompetitionAPIView.as_view()),
    path('competition/<int:pk>/', views.SpecificCompetitionAPIView.as_view()),
    path('competition/<int:pk>/delete/', views.UpdateAndDeleteCompetitionAPIView.as_view()),
    path('competition/<int:pk>/update/', views.UpdateAndDeleteCompetitionAPIView.as_view(), name='update'),


]