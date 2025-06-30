from django.shortcuts import render
from rest_framework.views import APIView 
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser
from django.core.mail import send_mail



# Create your views here.

class Hello(APIView):
    def get(self, request):
        return Response({"name": "Hello world!"})


class Email(APIView):
    parser_classes = [FormParser, MultiPartParser, JSONParser]
    def post(self, request):
        name = request.data.get("name")
        email = request.data.get("email")

        send_mail(subject="FUEL LOGISTICS", 
                  message=f"Hello {name},\n\nThank you for your interest in our products. We will get back to you soon.\n\nBest regards,\nYour Company",
                  from_email="idaraobong05@gmail.com", recipient_list=[email], fail_silently=False, auth_user="Idaraobong from py50", auth_password="bbdn inor sirg ypod")
        

        return Response ({"message": "Email sent successfully!"} , status=200)
