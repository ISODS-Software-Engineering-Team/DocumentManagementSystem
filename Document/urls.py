from django.urls import path

from . import views
from .views import UserRegisterView, UserLoginView,CompetitionListCreateView, get_all_competitions,update_competition,delete_competition

urlpatterns = [
    path('register', UserRegisterView.as_view(), name='register'),
    path('login', UserLoginView.as_view(), name='login'),
    path('documents', views.ListCreateDocumentView.as_view()),
    path('documents/<int:pk>', views.UpdateDeleteDocumentView.as_view()),
    path('category/<int:pk>', views.DeleteCategoryView.as_view()),
    path('update/<int:pk>/', views.UpdateCategoryView.as_view(), name='update-category'),
    path('competitions/', CompetitionListCreateView.as_view(), name='competition-list-create'),
    path('competitions/all', views.get_all_competitions, name='get_all_competitions'),
    path('competition/<int:competition_id>/update/', views.update_competition, name='update_competition'),
    path('competition/<int:competition_id>/delete/', views.delete_competition, name='delete_competition'),
    path('competition/<int:competition_id>/download/', views.FileDownloadAPIView.as_view(), name='retrieve')


]