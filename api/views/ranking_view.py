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

@api_view(['GET'])
def winners_view(request):
    winners = []

    project_votes = (
        Vote.objects.filter(category_type='project')
        .values('subcategory', 'project')
        .annotate(total_votes=Count('id'))
        .order_by('subcategory', '-total_votes')
    )

    seen_subs = set()
    for vote in project_votes:
        sub = vote['subcategory']
        if sub not in seen_subs:
            seen_subs.add(sub)
            project = Project.objects.get(id=vote['project'])
            winners.append({
                "type": "project",
                "subcategory": project.subcategory.name,
                "name": project.name,
                "votes": vote['total_votes'],
                "members": [
                    {
                        "name": m.name,
                        "classe": m.classe,
                        "email": getattr(m, "email", None)  
                    } for m in project.members.all()
                ]
            })

    stand_votes = (
        Vote.objects.filter(category_type='stand')
        .values('subcategory', 'stand')
        .annotate(total_votes=Count('id'))
        .order_by('subcategory', '-total_votes')
    )

    seen_subs = set()
    for vote in stand_votes:
        sub = vote['subcategory']
        if sub not in seen_subs:
            seen_subs.add(sub)
            stand = Stand.objects.get(id=vote['stand'])
            winners.append({
                "type": "stand",
                "subcategory": stand.category.name,
                "name": stand.name,
                "votes": vote['total_votes']
            })

    member_votes = (
        Vote.objects.filter(category_type='member')
        .values('subcategory', 'member')
        .annotate(total_votes=Count('id'))
        .order_by('subcategory', '-total_votes')
    )

    seen_subs = set()
    for vote in member_votes:
        sub = vote['subcategory']
        if sub not in seen_subs:
            seen_subs.add(sub)
            member = Member.objects.get(id=vote['member'])
            winners.append({
                "type": "member",
                "subcategory": member.classe,
                "name": member.name,
                "votes": vote['total_votes'],
                "classe": member.classe,
                "course": member.course
            })

    return Response({"winners": winners})
