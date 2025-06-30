from django.urls import path
from products.views import Hello, Email

urlpatterns = [
    path('greetings', Hello.as_view(), name='Hello'),
    path('email', Email.as_view(), name='Email'),

]