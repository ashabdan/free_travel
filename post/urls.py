from django.urls import path
from . import views


urlpatterns = [
    path('comments/', views.CommentListCreateView.as_view()),
    path('comments/<int:pk>/', views.CommentDetailView.as_view()),
    path('categories/', views.CategoryView.as_view()),
]
