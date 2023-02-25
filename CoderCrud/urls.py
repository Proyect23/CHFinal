"""CoderCrud URL Configuration

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
from django.contrib import admin
from django.urls import path
from Login import views
from django.conf.urls import handler404, handler500
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    #Main 
    path('', views.home, name='home'),
    
    #Terminos y condiciones
    path('policy&terms', views.Terminos_condicones, name='policy&terms'),
    
    #Admin
    path('admin/', admin.site.urls),
    
    #Rutas de los users
    path("login/", views.UserLogin, name='login'),
    path("logout/", views.CloseSession, name='logout'),
    
    #Rutas de las tareas CRUD
    path("task/", views.task, name='task'), #All
    path("task/complete", views.taskComplete, name='taskcomplete'), #Competed
    path("task/newtask/", views.newtask, name='newtask'), #Create
    path("task/<int:task_id>/", views.Taskdetails, name='taskdetails'), #Detail specific Task
    path("task/<int:task_id>/update", views.TaskUpdate, name='taskupdate'), #Update any Task
    path("task/<int:task_id>/delete", views.TaskDelete, name='taskdelete'), #Delete any Task
    
]
handler404 = views.error_404