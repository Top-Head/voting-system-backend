from rest_framework import serializers
from api.services.cloudinary import upload_to_cloudinary_members
from api.models import Vote, Voter, Member, Project, Category, Activity, SubCategory

class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        exclude = ['project']

class ProjectSerializer(serializers.ModelSerializer):
    members = MemberSerializer(many=True)
    class Meta:
        model = Project
        fields = ['id', 'name', 'subcategory', 'members', 'project_cover']

    def create(self, validated_data):
        members_data = validated_data.pop('members')
        project = Project.objects.create(**validated_data)
        for member_data in members_data:
            if "profile_cover" in member_data:
                image_file = member_data.pop("profile_cover")
                member_data['profile_image'] = upload_to_cloudinary_members(image_file)

            Member.objects.create(project=project, **member_data)
        return project
    
class SubCategorySerializer(serializers.ModelSerializer):
    projects = ProjectSerializer(many=True, read_only=True)
    class Meta:
        model = SubCategory
        fields = ['id', 'name', 'projects']

class CategorySerializer(serializers.ModelSerializer):
    subcategories = SubCategorySerializer(many=True, read_only=True)
    class Meta:
        model = Category
        fields = ['id', 'name', 'category_type', 'subcategories']


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
        fields = 'id', 'name', 'email', 'password'
