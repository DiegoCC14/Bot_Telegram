"""
URL configuration for Config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path
from .views import Home_Bot_Telegram , Files , Respuesta_Automatica , Respuesta_Automatica_Files , CronoJobs

urlpatterns = [
    path( '', Home_Bot_Telegram.as_view() , name='home' ),
    path( 'files/', Files.as_view() , name='files' ),
    path( 'respuestas_automaticas/', Respuesta_Automatica.as_view() , name='respuestas_automaticas' ),
    path( 'respuestas_automaticas_files/', Respuesta_Automatica_Files.as_view() , name='respuestas_automaticas_files' ),
    
    path( 'cronoojobs/', CronoJobs.as_view() , name='cronoojobs' ),
]
