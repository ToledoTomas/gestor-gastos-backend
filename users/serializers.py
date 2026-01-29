from rest_framework import serializers
from .models import UserProfile

class UserProfileSerializer(serializers.ModelSerializer):
  class Meta: 
    model = UserProfile
    fields = ['id', 'username', 'email', 'phone', 'money_preference']
    read_only_fields = ['id']

class UserRegistrationSerializer(serializers.ModelSerializer):
  password = serializers.CharField(write_only=True)

  class Meta:
    model = UserProfile
    fields = ['username', 'email', 'password', 'phone', 'money_preference']

  def create(self, validated_data):
    user = UserProfile(
      username=validated_data['username'],
      email=validated_data['email'],
      phone=validated_data.get('phone', ''),
      money_preference=validated_data.get('money_preference', 'USD')
    )
    user.set_password(validated_data['password'])
    user.save()
    return user
  
class UserLoginSerializer(serializers.Serializer):
  username = serializers.CharField()
  password = serializers.CharField(write_only=True)

class UserProfileUpdateSerializer(serializers.ModelSerializer):
  class Meta:
    model = UserProfile
    fields = ['email', 'phone', 'money_preference']
    read_only_fields = ['username']

  def update(self, instance, validated_data):
    instance.email = validated_data.get('email', instance.email)
    instance.phone = validated_data.get('phone', instance.phone)
    instance.money_preference = validated_data.get('money_preference', instance.money_preference)
    instance.save()
    return instance
