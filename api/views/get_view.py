from api import models
from rest_framework import status
from django.db.models import Count, Q
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from api.models import Category, Project, Voter, Vote, Member, Activity, SubCategory, Stand
from api.serializers import GetActivitySerializer, GetCategorySerializer, GetMemberSerializer, GetProjectSerializer, GetSubCategorySerializer, VoterSerializer, VoteSerializer

@cache_page(60 * 5)
@vary_on_cookie
@api_view(['GET'])
def count_project(request):
    project_count = Project.objects.count()
    return Response({"total": project_count}, status=status.HTTP_200_OK)

@cache_page(60 * 5)
@vary_on_cookie
@api_view(['GET'])
def count_voters(self):
    member_count = Member.objects.count()
    return Response({"total": member_count}, status=status.HTTP_200_OK)

@cache_page(60 * 5)
@vary_on_cookie
@api_view(['GET'])
def count_activity(request):
    activity_count = Activity.objects.count()
    return Response({"total": activity_count}, status=status.HTTP_200_OK)

@cache_page(60 * 5)
@vary_on_cookie
@api_view(['GET'])
def count_members(request):
    member_count = Member.objects.count()
    return Response({"total": member_count}, status=status.HTTP_200_OK)

@cache_page(60 * 5)
@vary_on_cookie
@api_view(['GET'])
def count_project_in_category(request, activity_id):
    try:
        activity = Activity.objects.get(id=activity_id)
    except Activity.DoesNotExist:
        return Response({"error": "Activity does not exist"}, status=status.HTTP_404_NOT_FOUND)
    
    category_count = (
        Category.objects
        .filter(activity_id=activity)
        .annotate(project_count=Count('projects'))
        .values("name", "project_count")   
    )    
    return Response({"Total": list(category_count)}, status=status.HTTP_200_OK)

@cache_page(60 * 5)
@vary_on_cookie
@api_view(["GET"])
def activity_project_count(request, activity_id):
    try:
        activity = (
            Activity.objects
            .filter(id=activity_id)
            .annotate(project_count=Count("projects"))
            .values("project_count")
            .first()
        )

        if not activity:
            return Response({"error": "Activity not found"}, status=404)

        return Response(activity, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@cache_page(60 * 5)
@vary_on_cookie
@api_view(['GET'])
def get_projects(request):
    projects = Project.objects.all()
    serializer = GetProjectSerializer(projects, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@cache_page(60 * 5)
@vary_on_cookie
@api_view(['GET'])
def get_project(request, project_id):
    try:
        project = Project.objects.get(id=project_id)
    except Project.DoesNotExist:
        return Response({"error": "Project not found"}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = GetProjectSerializer(project)
    return Response(serializer.data, status=status.HTTP_200_OK)

@cache_page(60 * 5)
@vary_on_cookie
@api_view(['GET'])
def get_categories_by_activity(request, activity_id):
    categories = Category.objects.filter(activity_id=activity_id)
    serializer = GetCategorySerializer(categories, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@cache_page(60 * 5)
@vary_on_cookie
@api_view(['GET'])
def get_category(request, category_id):
    try:
        category = Category.objects.get(id=category_id)
    except Category.DoesNotExist:
        return Response({"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = GetCategorySerializer(category)
    return Response(serializer.data, status=status.HTTP_200_OK)

@cache_page(60 * 5)
@vary_on_cookie
@api_view(['GET'])
def get_category_items(request):
     response = []
     category_id = int(request.GET.get('cat_id', 0))
     subcategory_id = int(request.GET.get('subcat_id', 0))
     category_type = request.GET.get('cat_tp', '')
     activity_id = int(request.GET.get('act_id', 0))


     if not request.user.is_authenticated:
        return Response({"error": "Authentication required."}, status=status.HTTP_401_UNAUTHORIZED)
     
     user = request.user
     activity = Activity.objects.filter(id=activity_id).first()

     if category_id and subcategory_id:
        if category_type == 'project':
            projects = Project.objects.filter(subcategory__id=subcategory_id, activity__id=activity.id)

            for proj in projects:
                has_voted = Vote.objects.filter(voter=user, category__id=category_id, subcategory__id=subcategory_id, project=proj, activity__id=activity.id).exists()
                response.append(
                    {
                        "id": proj.id,
                        "name": proj.name.encode('utf-8'),
                        "cover": None,
                        "activity": proj.activity.name.encode('utf-8'),
                        "classe": None,
                        "turma": None,
                        "course": None,
                        "has_voted": has_voted
                    }
                )

        elif category_type == 'member':
            members = Member.objects.filter(subcategory__id=subcategory_id, activity__id=activity.id)

            for member in members:
                has_voted = Vote.objects.filter(voter=user, category__id=category_id,subcategory__id=subcategory_id, member=member, activity__id=activity.id).exists()
                response.append(
                    {
                        "id": member.id,
                        "name": member.name.encode('utf-8'),
                        "cover": member.profile_image.url,
                        "classe": member.classe.encode('utf-8'),
                        "turma": member.turma,
                        "course": member.course.encode('utf-8'),
                        "activity": member.activity.name.encode('utf-8'),
                        "type": category_type,
                        "has_voted": has_voted
                    }
                )

        return Response({"data": response}, status=status.HTTP_200_OK)

     elif category_id:
        if category_type == 'member':
            members = Member.objects.filter(category__id=category_id, activity__id=activity.id)

            for member in members:
                has_voted = Vote.objects.filter(voter=user, category__id=category_id, member=member, activity__id=activity.id).exists()
                response.append(
                    {
                        "id": member.id,
                        "name": member.name.encode('utf-8'),
                        "cover": member.profile_image.url,
                        "classe": member.classe.encode('utf-8'),
                        "turma": member.turma,
                        "course": member.course.encode('utf-8'),
                        "activity": member.activity.name.encode('utf-8'),
                        "type": category_type,
                        "has_voted": has_voted
                    }
                )

        elif category_type == 'stand':
            stands = Stand.objects.filter(category__id=category_id, activity__id=activity.id)

            for stand in stands:
                has_voted = Vote.objects.filter(voter=user, category__id=category_id, stand=stand, activity__id=activity.id).exists()
                response.append(
                    {
                        "id": stand.id,
                        "name": stand.name.encode('utf-8'),
                        "cover": stand.stand_cover.url,
                        "activity": stand.activity.name.encode('utf-8'),
                        "type": category_type,
                        "classe": None,
                        "turma": None,
                        "course": None,
                        "has_voted": has_voted
                    }
                )

        return Response({"data": response}, status=status.HTTP_200_OK)

@cache_page(60 * 5)
@vary_on_cookie
@api_view(['GET'])
def get_members(request):
    members = Member.objects.all()
    serializer = GetMemberSerializer(members, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@cache_page(60 * 5)
@vary_on_cookie
@api_view(['GET'])
def get_member(request, member_id):
    try:
        member = Member.objects.filter(id=member_id)
    except Member.DoesNotExist:
        return Response({"error": "Member not found"}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = GetMemberSerializer(member)
    return Response(serializer.data, status=status.HTTP_200_OK)

@cache_page(60 * 5)
@vary_on_cookie
@api_view(['GET'])
def get_me(request):
    voter_id = request.user.id

    try:
        voter = Voter.objects.get(id=voter_id)
    except Voter.DoesNotExist:
        return Response({"error": "Voter not found"}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = VoterSerializer(voter)
    return Response(serializer.data, status=status.HTTP_200_OK)

@cache_page(60 * 5)
@vary_on_cookie
@api_view(['GET'])
def get_subcategories(request):
    subcategories = SubCategory.objects.all()
    serializer = GetSubCategorySerializer(subcategories, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@cache_page(60 * 5)
@vary_on_cookie
@api_view(['GET'])
def get_subcategory(request, id):
    try:
        subcategory = SubCategory.objects.get(id=id)
    except SubCategory.DoesNotExist:
        return Response({"error": "Subcategory not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = GetSubCategorySerializer(subcategory)
    return Response(serializer.data, status=status.HTTP_200_OK)

@cache_page(60 * 5)
@vary_on_cookie
@api_view(['GET'])
def get_members_by_category(request, category_id):
    try:
        category = Category.objects.get(id=category_id)
    except Category.DoesNotExist:
        return Response({"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND)
    
    members = Member.objects.filter(project__category=category)
    serializer = GetMemberSerializer(members, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@cache_page(60 * 5)
@vary_on_cookie
@api_view(['GET'])
def get_votes(request):
    votes = Vote.objects.all()
    serializer = VoteSerializer(votes, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@cache_page(60 * 5)
@vary_on_cookie
@api_view(['GET'])
def get_activities(request):
    activitys = Activity.objects.all()
    serializer = GetActivitySerializer(activitys, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@cache_page(60 * 5)
@vary_on_cookie
@api_view(['GET'])
def get_activity(request, activity_id):
    try:
        activity = Activity.objects.get(id=activity_id)
    except Activity.DoesNotExist:
        return Response({"error": "Activity not found"}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = GetActivitySerializer(activity)
    return Response(serializer.data, status=status.HTTP_200_OK)

@cache_page(60)
@vary_on_cookie
@api_view(["GET"])
def top_projects(request):
    projects = (
        Project.objects
        .annotate(vote_count=Count("vote", filter=Q(vote__project__isnull=False)))
        .order_by("-vote_count")[:5]
    )

    data = [
        {
            "name": project.name,
            "vote_count": project.vote_count
        }
        for project in projects
    ]

    return Response(data, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_members_by_subcategory(request, subcategory_id):
    try:
        members = Member.objects.filter(subcategory_id=subcategory_id)
        if not members.exists():
            return Response(
                {"message": "Nenhum membro encontrado para esta subcategoria."},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = GetMemberSerializer(members, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    except Exception as e:
        return Response(
            {"error": f"Erro ao buscar membros: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
