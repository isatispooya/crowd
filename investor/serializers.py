from rest_framework import serializers
from django.contrib.auth import get_user_model
from . import models

User = get_user_model()

class CartSerializer (serializers.ModelSerializer):
    class Meta:
        model = models.Cart
        fields = '__all__'
        read_only_fields = ['user']  # جلوگیری از تغییر کاربر توسط کاربر


