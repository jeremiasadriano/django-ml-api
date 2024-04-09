from django.urls import path
from . import views as view

urlpatterns = [
    path('register/', view.register, name="register"),
    path('login/', view.login, name='login'),
    path('chat/', view.chat, name='chat')
] 