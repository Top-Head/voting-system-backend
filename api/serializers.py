from rest_framework import serializers
from api.models import Category, Vote, Voter, Competitor

class CompetitorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Competitor
        field = '__all__'

class VoterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Voter
        field = '__all__'

class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        field = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        field = '__all__'