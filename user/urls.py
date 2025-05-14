from django.urls import include, path
from .views import signup_view, login_view, logout_view, password_reset_view, home_view, mypage_view
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', login_view, name='login'),  
    path('signup/', signup_view, name='signup'),
    path('logout/', logout_view, name='logout'),
    path('password-reset/', password_reset_view, name='password_reset'),
     path('home/', login_required(home_view), name='home'), 
    path('mypage/', login_required(mypage_view), name='mypage'),

]