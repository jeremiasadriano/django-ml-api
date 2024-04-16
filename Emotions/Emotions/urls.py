from django.contrib import admin
from django.urls import path, include
from Person.urls import view

urlpatterns = [
    path('',view.chat, name='home'),
    path('',include('Person.urls')),
    path('admin/', admin.site.urls)
]
