from django.urls import path
from . import views as view

urlpatterns = [
    path('register/', view.register, name="register"),
    path('login/', view.login, name='login'),
    path('update/', view.update, name='update'),
    path('delete',view.delete, name='delete'),
    path('chat/', view.chat, name='chat'),
    path('logout',view.logout_view,name='logout')
] 