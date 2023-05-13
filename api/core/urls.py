from django.urls import path, include
from . import views


urlpatterns = [
    path('auth/', include('auth_user.urls')),
]