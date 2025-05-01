from rest_framework import serializers
from api.models import Vote, Voter, Member, Project, Category, Activity
from api.services.cloudinary import upload_to_cloudinary_members, upload_to_cloudinary_projects

class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        exclude = ['project']

    def create(self, validated_data):
        if 'profile_image' in validated_data:
            validated_data['profile_image'] = upload_to_cloudinary_members(validated_data['profile_image'])
        return super().create(validated_data)

class ProjectSerializer(serializers.ModelSerializer):
    members = MemberSerializer(many=True)

    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'category', 'project_cover', 'members']

    def create(self, validated_data):
        members_data = validated_data.pop('members')
        if 'project_cover' in validated_data:
            validated_data['project_cover'] = upload_to_cloudinary_projects(validated_data['project_cover'])
        project = Project.objects.create(**validated_data)
        for member_data in members_data:
            if 'profile_image' in member_data:
                member_data['profile_image'] = upload_to_cloudinary_members(member_data['profile_image'])
            Member.objects.create(project=project, **member_data)
        return project
    
class CategorySerializer(serializers.ModelSerializer):
    projects = ProjectSerializer(many=True, read_only=True)
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'projects']

    def create(self, validated_data):
        projects_data = validated_data.pop('projects')
        category = Category.objects.create(**validated_data)
        for project_data in projects_data:
            Project.objects.create(category=category, **project_data)
        return category
    
class ActivitySerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)

    class Meta:
        model = Activity
        fields = ['id', 'name', 'description', 'categories']

    def create(self, validated_data):
        categories_data = validated_data.pop('categories')
        activity = Activity.objects.create(**validated_data)
        for category_data in categories_data:
            Category.objects.create(activity=activity, **category_data)
        return activity
    
class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = '__all__'
