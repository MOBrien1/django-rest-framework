from django.shortcuts import render
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, permissions
from .models import CustomUser, UserProfile
from .serializers import CustomUserSerializer, UserProfileSerializer
from django_filters.rest_framework import DjangoFilterBackend


class CustomUserDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated|ReadOnly]
    queryset = CustomUser.objects.all() 
    serializer_class = CustomUserSerializer

class CustomUserList(generics.ListCreateAPIView):
    permission_classes = [ReadOnly]
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [ 
            'username',
    ]

class UserProfileList(generics.ListCreateAPIView):
    permission_classes = [ReadOnly]
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [ 
            'username',
            'location',
            'organisation'
    ]

class UserProfileDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated|ReadOnly]
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    
