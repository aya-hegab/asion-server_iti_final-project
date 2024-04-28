from django.urls import path
from .views import ContactMessageListCreateView

urlpatterns = [
    path('contact/', ContactMessageListCreateView.as_view(), name='contact-list-create'),
]