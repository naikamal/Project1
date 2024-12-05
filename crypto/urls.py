from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Homepage
    path('encrypt/', views.encrypt, name='encrypt'),  # Encryption
    path('decrypt/', views.decrypt, name='decrypt'),  # Decryption
]