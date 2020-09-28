from rest_framework import serializers
from .models import CustomUser, UserProfile

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'    

    def create(self, validated_data):
        return CustomUser.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.save()
        return instance

    def delete(self, validated_data):
        return CustomUser.objects.delete(**validated_data)

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'

    def create(self, validated_data):
        return UserProfile.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.bio = validated_data.get('bio', instance.bio)
        instance.profile_pic = validated_data.get('profile_pic', instance.profile_pic)
        instance.pet_pic = validated_data.get('pet_pic', instance.pet_pic)
        instance.location = validated_data.get('location', instance.location)
        instance.organisation = validated_data.get('organisation', instance.organisation)
        instance.save()
        return instance
    
    def delete(self, validated_data):
        return UserProfile.objects.delete(**validated_data)
