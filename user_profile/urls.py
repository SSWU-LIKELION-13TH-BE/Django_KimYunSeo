from django.urls import path
from . import views

urlpatterns = [
    path('<str:username>/', views.profile_view, name='profile_view'),
    path('my/guestbook/', views.my_guestbook_view, name='my_guestbook'),
]
