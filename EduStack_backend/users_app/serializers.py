from rest_framework import serializers
from .models import User




class UserSerializers(serializers.ModelSerializer):
    class Meta:
        models = User
        fields = '__all__'




