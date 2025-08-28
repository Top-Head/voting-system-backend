from rest_framework import status
from django.db.models import Count
from rest_framework.response import Response
from rest_framework.decorators import api_view
from api.models import Category, Project, Voter, Vote, Member, Activity, SubCategory, Stand
from api.serializers import ProjectSerializer,CategorySerializer,MemberSerializer,VoteSerializer,ActivitySerializer,VoterSerializer,SubCategorySerializer

@api_view(['GET'])
def count_project(request):
    project_count = Project.objects.count()
    return Response({"total": project_count}, status=status.HTTP_200_OK)

@api_view(['GET'])
def count_project_in_category(request, activity_id):
    try:
        activity = Activity.objects.get(id=activity_id)
    except Activity.DoesNotExist:
        return Response({"error": "Activity does not exist"})
    
    category_count = Category.objects.filter(activity_id=activity).annotate(project_count=Count('projects'))
    
    return Response({"Total": category_count}, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_projects(request):
    projects = Project.objects.all()
    serializer = ProjectSerializer(projects, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_project(request, id):
    try:
        project = Project.objects.get(id=id)
    except Project.DoesNotExist:
        return Response({"error": "Project not found"}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = ProjectSerializer(project)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def count_category(request):
    category_count = Category.objects.count()
    return Response({"total": category_count},status=status.HTTP_200_OK)

@api_view(['GET'])
def get_categorys(request):
    category = Category.objects.all()
    serializer = CategorySerializer(category, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

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

@api_view(['GET'])
def get_members(request):
    members = Member.objects.all()
    serializer = MemberSerializer(members, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_member(request, member_id):
    try:
        member = Member.objects.filter(id=member_id)
    except Member.DoesNotExist:
        return Response({"error": "Member not found"}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = MemberSerializer(member)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_me(request):
    voter_id = request.user.id

    try:
        voter = Voter.objects.get(id=voter_id)
    except Voter.DoesNotExist:
        return Response({"error": "Voter not found"}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = VoterSerializer(voter)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_subcategories(request):
    subcategories = SubCategory.objects.all()
    serializer = SubCategorySerializer(subcategories, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_subcategory(request, id):
    try:
        subcategory = SubCategory.objects.get(id=id)
    except SubCategory.DoesNotExist:
        return Response({"error": "Subcategory not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = SubCategorySerializer(subcategory)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_members_by_category(request, category_id):
    try:
        category = Category.objects.get(id=category_id)
    except Category.DoesNotExist:
        return Response({"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND)
    
    members = Member.objects.filter(project__category=category)
    serializer = MemberSerializer(members, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_votes(request):
    votes = Vote.objects.all()
    serializer = VoteSerializer(votes, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_activities(request):
    activitys = Activity.objects.all()
    serializer = ActivitySerializer(activitys, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_activity(request, id):
    try:
        activity = Activity.objects.get(id=id)
    except Activity.DoesNotExist:
        return Response({"error": "Activity not found"}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = ActivitySerializer(activity)
    return Response(serializer.data, status=status.HTTP_200_OK)