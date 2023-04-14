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
    path('competitions/', views.get_all_competitions, name='get_all_competitions'),
    path('competition/<int:id>/', views.update_competition, name='update_competition'),
    path('competition/<int:id>/', views.delete_competition, name='delete_competition')

]