from rest_framework import serializers
from api.models import Vote, Voter, Member, Project, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']  

class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        exclude = ['project']  


class ProjectSerializer(serializers.ModelSerializer):
    members = MemberSerializer(many=True)

    class Meta:
        model = Project
        fields = ['id', 'name', 'email', 'description', 'category', 'project_cover', 'members']

    def create(self, validated_data):
        members_data = validated_data.pop('members')
        project = Project.objects.create(**validated_data)
        for member_data in members_data:
            Member.objects.create(project=project, **member_data)
        return project