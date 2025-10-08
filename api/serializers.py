from rest_framework import serializers
from api.models import Vote, Voter, Member, Project, Category, Activity, SubCategory, Stand

#-------------------------------------------POST SERIALIZERS----------------------------------

class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ['id', 'name', 'classe', 'turma', 'profile_image', 'course', 'activity', 'project', 'category', 'subcategory']

class StandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stand
        fields = ['id', 'name', 'stand_cover', 'activity', 'category']

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'activity', 'category', 'subcategory', 'project_cover']
    
class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ['id', 'name', 'activity', 'category']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'category_type', 'activity']

class ActivitySerializer(serializers.ModelSerializer):
    start_date = serializers.DateField(
        format="%d-%m-%Y", input_formats=["%d-%m-%Y", "%Y-%m-%d"], required=False
    )
    end_date = serializers.DateField(
        format="%d-%m-%Y", input_formats=["%d-%m-%Y", "%Y-%m-%d"], required=False
    )

    class Meta:
        model = Activity
        fields = ['id', 'name', 'description', 'start_date', 'end_date', 'finished']

class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = '__all__'

class VoterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Voter
        fields = 'id', 'name', 'email', 'password'

#---------------------------------------------- GET SERIALIZERS-------------------------------

class GetMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        exclude = ['project']

class GetProjectSerializer(serializers.ModelSerializer):
    members = MemberSerializer(many=True)
    class Meta:
        model = Project
        fields = ['id', 'name', 'subcategory', 'members', 'project_cover']

class GetSubCategorySerializer(serializers.ModelSerializer):
    projects = ProjectSerializer(many=True, read_only=True)
    class Meta:
        model = SubCategory
        fields = ['id', 'name', 'projects']

class GetCategorySerializer(serializers.ModelSerializer):
    subcategories = SubCategorySerializer(many=True, read_only=True)
    class Meta:
        model = Category
        fields = ['id', 'name', 'category_type', 'subcategories']


class GetActivitySerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True)
    start_date = serializers.DateField(
        format="%d-%m-%Y", input_formats=["%d-%m-%Y"], required=False
    )
    end_date = serializers.DateField(
        format="%d-%m-%Y", input_formats=["%d-%m-%Y"], required=False
    )

    class Meta:
        model = Activity
        fields = ['id', 'name', 'description', 'start_date', 'end_date', 'categories']