from rest_framework import serializers
from .models import (
    Project, 
    Pledge, 
    Donations, 
    Category,
)

class ProjectSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    title = serializers.CharField(max_length=200)
    description = serializers.CharField(max_length=500)
    post_code = serializers.CharField(max_length=200)
    suburb = serializers.CharField(max_length=50)
    seeking = serializers.CharField(max_length=200)
    image = serializers.URLField()
    is_open = serializers.BooleanField()
    date_created = serializers.DateTimeField()
    owner = serializers.ReadOnlyField(source='owner.id')
    
    def create(self, validated_data):
        return Project.objects.create(**validated_data)
    
    #dont think this needs delete
    
    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.seeking = validated_data.get('seeking', instance.seeking)
        instance.post_code = validated_data.get('post_code', instance.post_code)
        instance.suburb = validated_data.get('suburb', instance.suburb)
        instance.image = validated_data.get('image', instance.image)
        instance.is_open = validated_data.get('is_open', instance.is_open)
        instance.date_created = validated_data.get('date_created', instance.date_created)
        instance.owner = validated_data.get('owner', instance.owner)
        instance.save()
        return instance
    

class PledgeSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    comment = serializers.CharField(max_length=200)
    anonymous = serializers.BooleanField()
    project_id = serializers.IntegerField()
    supporter = serializers.ReadOnlyField(source='supporter.id')
    category = serializers.PrimaryKeyRelatedField(queryset = Category.objects.all())

    def create(self, validated_data):
        return Pledge.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.comment = validated_data.get('comment', instance.comment)
        instance.save()
        return instance

    def delete(self, validated_data):
        return Pledge.objects.delete(**validated_data)

class ProjectDetailSerializer(ProjectSerializer):
    pledges = PledgeSerializer(many=True, read_only=True)

    def create(self, validated_data):
        return Pledge.objects.create(**validated_data)

    def delete(self, validated_data):
        return Pledge.objects.delete(**validated_data)

#Supporter field not right ID is not OWNER 
class DonationsSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    item = serializers.CharField(max_length=200)
    quantity = serializers.IntegerField()
    img = serializers.URLField()
    location = serializers.CharField(max_length=200)
    supporter = serializers.ReadOnlyField(source='supporter.username')
    
    def create(self, validated_data):
        return Donations.objects.create(**validated_data)
    
    def delete(self, validated_data):
        return Donations.objects.delete(**validated_data)

class DonationItemsSerializer(DonationsSerializer):
    id = serializers.ReadOnlyField()
    item = serializers.CharField(max_length=100)

    def create(self, validated_data):
        return DonationItems.objects.create(**validated_data)
   
    def update(self, instance, validated_data):
        instance.item = validated_data.get('item', instance.item)

    def delete(self, validated_data):
        return Donations.objects.delete(**validated_data)

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

    def create(self, validated_data):
        return Category.objects.create(**validated_data)

    def delete(self, validated_data):
        return Category.objects.delete(**validated_data)
