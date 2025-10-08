from rest_framework import status
from django.db.models import Count
from rest_framework.views import APIView
from api.serializers import VoterSerializer
from rest_framework.response import Response
from api.features import generate_vote_ranking
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from api.models import Project, Voter, Activity, SubCategory

class VoterListView(APIView):
    
    @method_decorator(cache_page(60 * 3))
    @method_decorator(vary_on_cookie)
    def get(self, request):
        try:
            voters = Voter.objects.all()
            serializer = VoterSerializer(voters, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class RankingView(APIView):

    @method_decorator(cache_page(60 * 3))
    @method_decorator(vary_on_cookie)
    def get(self, request, activity_id):

        activites = Activity.objects.filter(id=activity_id).first()

        if not activites.finished:
            return Response({"msg": "Rank is not avaible now"}, status=status.HTTP_403_FORBIDDEN)
        
        rankings = generate_vote_ranking(activity_id)

        return Response(rankings, status=status.HTTP_200_OK)

class PublicRankingView(APIView):
    authentication_classes = []  
    permission_classes = []      

    @method_decorator(cache_page(60 * 3))
    @method_decorator(vary_on_cookie)
    def get(self, request, activity_id):
        activity = Activity.objects.filter(id=activity_id).first()

        if not activity:
            return Response({"error": "Activity not found"}, status=status.HTTP_404_NOT_FOUND)
        
        if activity.finished:
            return Response({"msg": "Rank is not avaible now"}, status=status.HTTP_403_FORBIDDEN)
        rankings = generate_vote_ranking(activity_id)
        return Response(rankings, status=status.HTTP_200_OK)

class VerifyActivity(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, activity_id):
        activity = Activity.objects.filter(id=activity_id).first()
        if not activity:
            return Response({"error": "Activity not found"}, status=status.HTTP_404_NOT_FOUND)

        return Response({"is_finished": activity.finished}, status=status.HTTP_200_OK)

class SubcategoryProjectRankingView(APIView):

    @method_decorator(cache_page(60 * 3))
    @method_decorator(vary_on_cookie)
    def get(self, request, subcategory_id):
        try:
            subcategory = SubCategory.objects.get(id=subcategory_id)
        except SubCategory.DoesNotExist:
            return Response({"error": "Subcategory not found"}, status=status.HTTP_404_NOT_FOUND)

        projects = Project.objects.filter(subcategory=subcategory).annotate(vote_count=Count('vote')).order_by('-vote_count')

        data = []
        for project in projects:
            members = project.members.all() if hasattr(project, 'members') else project.member_set.all()
            members_data = [
                {
                    'name': member.name,
                    'classe': member.classe,
                    'turma': member.turma
                }
                for member in members
            ]
            data.append({
                'project_id': project.id,
                'name': project.name,
                'description': project.description,
                'subcategory_name': subcategory.name,
                'category_name': project.category.name if project.category else None,
                'votes': project.vote_count,
                'members': members_data
            })
        return Response(data, status=status.HTTP_200_OK)