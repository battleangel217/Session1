from rest_framework import serializers
from .models import Products


class Product_serializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        field = '__all__'
