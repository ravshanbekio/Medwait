from django.urls import path
from .views import signup, signin, signout

urlpatterns = [
    path('register/',signup, name='register'),
    path('login/',signin, name='login'),
    path('logout/',signout, name='logout'),
]