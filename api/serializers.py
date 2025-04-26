from rest_framework import serializers
from api.models import Vote, Voter, Member, Project, Category


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        exclude = ['project']  


class ProjectSerializer(serializers.ModelSerializer):
    members = MemberSerializer(many=True)

    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'category', 'project_cover', 'members']

    def create(self, validated_data):
        members_data = validated_data.pop('members')
        project = Project.objects.create(**validated_data)
        for member_data in members_data:
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
    