from django.http import Http404
from rest_framework import status, permissions, generics
from django_filters.rest_framework import DjangoFilterBackend
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
from .permissions import IsOwnerOrReadOnly, IsAuthenticatedOrReadOnly


class ProjectList(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
            'title', 
            'is_open',
            'date_created',
            'post_code',
            'owner',
            'suburb',
    ]

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
            project = Project.objects.get(pk=pk)
            self.check_object_permissions(self.request, project)
            return project
        except Project.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        project = self.get_object(pk)
        serializer = ProjectDetailSerializer(project)
        try:
            return Response(
            serializer.data,
            status=status.HTTP_200_OK
            )
        except Project.DoesNotExist:
            raise Http404

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
            return Response(status=status.HTTP_200_OK)
        
    
    def delete(self, request, pk):
        project = self.get_object(pk)
        self.check_object_permissions(request, project)
        project.delete()
        return Response(status=status.HTTP_200_OK)


class PledgeList(APIView):
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['supporter', 'category' ]

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
            serializer.save(supporter=request.user)
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


class DonationsItem(APIView):
    def get(self, request):
        items = self.get_object(items)
        serializer = DonationsSerializer()
        if serializer.is_valid():
            serializer.save()
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
        
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
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [ 
            'item',
            'supporter',
            'location',
    ]


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

class CategoryList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
            'name', 
    ]