"""ai_agro_predictor URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from fertilizer_predictor import views
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('cadastro/', views.signup, name='signup'),
    path('entrar/', views.signin, name='signin'),
    path('sair/', views.signout, name='signout'),
    path('recomendar/', views.predictor, name='predictor'),
    path('resultado/<int:id_resultado>/', views.result, name='result'),
    path('historico/', views.history, name='history'),
]
