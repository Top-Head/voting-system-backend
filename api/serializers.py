from rest_framework import serializers
from api.models import Vote, Voter, Member, Project, Category, Activity

class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        exclude = ['project']

class ProjectSerializer(serializers.ModelSerializer):
    members = MemberSerializer(many=True)
    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'category', 'members']

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
        fields = ['id', 'name', 'projects']


class ActivitySerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True)
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

class VoterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Voter
        fields = '__all__'
