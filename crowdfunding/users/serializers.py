from rest_framework import serializers
from .models import CustomUser, UserProfile
from projects.serializers import PledgeSerializer, ProjectSerializer

class CustomUserSerializer(serializers.ModelSerializer):
    owner_projects = ProjectSerializer(many=True, read_only=True)
    pledges = PledgeSerializer(many=True, read_only=True)

    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'owner_projects', 'pledges', 'password')   
        extra_kwargs = {'password': {'write_only': True}}
        
    def create(self, validated_data):
        # create the profile - you can pass in any fields that are required here:
        user = super(CustomUserSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        print(validated_data)
        return user
        
        # user = CustomUser.objects.create_user(
        #     username=validated_data['username'],
        #     email=validated_data['email'],
        #     password=validated_data['password']
        # )
        # return user

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.set_password(validated_data['password', instance.password])

        profile_data = validated_data.pop('profile', {})
        for (key, value) in validated_data.items():
            setattr(instance, key, value)
        instance.save()

        for (key, value) in profile_data.items():
            setattr(instance.profile, key, value)
        instance.profile.save()
        return instance

    def delete(self, validated_data):
        return CustomUser.objects.delete(**validated_data)

class UserProfileSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)

    class Meta:
        model = UserProfile
         # better to specify fields
        fields = ('user','bio', 'profile_pic', 'pet_pic', 'location', 'organisation')
           
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
