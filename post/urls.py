from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('create/', views.post_create, name='post_create'),
    path('<int:pk>/', views.post_detail, name='post_detail'),
    path('<int:pk>/comment/', views.add_comment, name='add_comment'),
    path('<int:pk>/like/', views.toggle_post_like, name='toggle_post_like'),
    path('comment/<int:pk>/like/', views.toggle_comment_like, name='toggle_comment_like'),
    
]
