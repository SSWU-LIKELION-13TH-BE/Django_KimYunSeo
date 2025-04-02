"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include

def redirect_to_home(request):
    return redirect('home')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('user.urls')),  # 유저 관련 URL들
    path('', redirect_to_home),  # 기본 페이지 접근 시 home으로 이동
     path('home/', include('user.urls')),
]