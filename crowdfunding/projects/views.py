from django.http import Http404
from rest_framework import status, permissions, generics
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Project, Pledge, Donations, Category
from .serializers import (
    ProjectSerializer, 
    CategorySerializer, 
    PledgeSerializer, 
    ProjectDetailSerializer, 
    DonationsSerializer, 
    DonationItemsSerializer
)
from .permissions import IsOwnerOrReadOnly
# Create your views here.

class ProjectList(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def get(self, request):
        projects = Project.objects.all()
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)

    def post (self, request):
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

class ProjectDetail(APIView):
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly
        ]
    def get_object(self, pk):
        try:
            return Project.objects.get(pk=pk)
        except Project.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        project = self.get_object(pk)
        self.check_object_permissions(request, project)
        serializer = ProjectDetailSerializer(project)
        return Response(
            serializer.data,
            status=status.HTTP_200_OKAY
            )

    def put(self, request, pk):
        project = self.get_object(pk)
        self.check_object_permissions(request, project)
        data = request.data
        serializer = ProjectDetailSerializer(
            instance=project,
            data=data,
            partial=True
          )
        if serializer.is_valid():
            serializer.save()
    
    def delete(self, request, pk):
        project = self.get_object(pk)
        self.check_object_permissions(request, project)
        project.delete()
        return Response(status=status.HTTP_200_OK)

class PledgeList(APIView):
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly
        ]

    def get(self, request):
        pledges = Pledge.objects.all()
        serializer = PledgeSerializer(pledges, many=True)
        return Response(serializer.data)

    def post (self, request):
        serializer = PledgeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, pk):
        pledge = self.get_object(pk)
        pledge.delete()
        return Response(status=status.HTTP_200_OK)

class DonationsList(APIView):
    def get(self, request):
        donations = Donations.objects.all()
        serializer = DonationsSerializer(donations, many=True)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK)
    
    def post (self, request):
        serializer = DonationsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

class DonationItemsList(APIView):

    def get(self, request):
        Items = DonationItems.objects.all()
        serializer = DonationItemsSerializer(Items, many=True)
        return Response(serializer.data)

    def post (self, request):
        serializer = DonationItemsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

class CategoryList(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
