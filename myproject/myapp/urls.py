from django.urls import path
from .views import home, ask  # Import the views you've defined

urlpatterns = [
    path('', home, name='home'),  # Home page
    path('ask', ask, name='ask'),  # Path for the 'ask' functionality
]
