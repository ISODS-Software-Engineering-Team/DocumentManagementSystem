from django.urls import path

from . import views
from .views import CategoryListView, RetrieveCategoryView, UserRegisterView, UserLoginView

urlpatterns = [
    path('register', UserRegisterView.as_view(), name='register'),
    path('login', UserLoginView.as_view(), name='login'),
    path('documents', views.ListCreateDocumentView.as_view()),
    path('documents/<int:pk>', views.UpdateDeleteDocumentView.as_view()),
    path('category/<int:pk>', views.DeleteCategoryView.as_view()),
     path('categories/', CategoryListView.as_view(), name='category-list'),
     path('categories/<int:pk>/', RetrieveCategoryView.as_view(), name='category-detail'),
]