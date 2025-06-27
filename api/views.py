from dal import autocomplete
from typing import Optional, Type
from rest_framework import status
from django.db.models import Count
from api.features import generate_vote_ranking
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny
from django.views.decorators.csrf import csrf_exempt
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import make_password, check_password
from api.models import Category, Project, Voter, Vote, Member, Activity, SubCategory, Stand
from api.serializers import ProjectSerializer, CategorySerializer, MemberSerializer, VoteSerializer, ActivitySerializer, VoterSerializer, SubCategorySerializer


# Create your views here.
class ActivityAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Activity.objects.all()
        if self.q:
            qs = qs.filter(name__icontains=self.q)
        return qs

class CategoryAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Category.objects.all()

        activity_id = self.forwarded.get('activity') or self.request.GET.get('activity')
        if activity_id:
            qs = qs.filter(activity_id=activity_id)

        if self.q:
            qs = qs.filter(name__icontains=self.q)

        return qs

class SubCategoryAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = SubCategory.objects.all()
        category_id = self.forwarded.get('category') or self.request.GET.get('category')
        if category_id:
            qs = qs.filter(category_id=category_id)
        if self.q:
            qs = qs.filter(name__icontains=self.q)
        return qs

@api_view(['POST'])
def create_activity(request):
    serializer = ActivitySerializer(data=request.data)

    if serializer.is_valid():
        activity = serializer.save()
        return Response({
            "message": "Atividade criada com sucesso!",
            "activity": ActivitySerializer(activity).data
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PATCH'])
def close_activity(request, id):
    try:
        activity = Activity.objects.get(id=id)
    except Activity.DoesNotExist:
        return Response({"error": "Activity not found"}, status=status.HTTP_404_NOT_FOUND)

    activity.finished = True
    activity.save()

    return Response({"message": "Activity closed successfully"}, status=status.HTTP_200_OK)

@api_view(['POST'])
def create_project(request):
    serializer = ProjectSerializer(data=request.data)

    if serializer.is_valid():
        project = serializer.save()
        return Response({
            "message": "Projeto criado com sucesso!",
            "project": ProjectSerializer(project).data
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def update_project(request, id):
    try:
        project = Project.objects.get(id=id)
    except Project.DoesNotExist:
        return Response({"error": "Project not found"}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = ProjectSerializer(instance=project, data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def create_subcategory(request):
    serializer = SubCategorySerializer(data=request.data)

    if serializer.is_valid():
        subcategory = serializer.save()
        return Response({
            "message": "Subcategoria criada com sucesso!",
            "subcategory": SubCategorySerializer(subcategory).data
        }, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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

@csrf_exempt
@api_view(['POST'])  
def voter_login(request):
    email = request.data.get('email')
    password = request.data.get('password')

    if not email or not password:
        return Response({"error": "Email and password required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        voter = Voter.objects.get(email=email)
    except Voter.DoesNotExist:
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

    if not check_password(password, voter.password):
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

    refresh = RefreshToken.for_user(voter)
    refresh['email'] = voter.email
    access_token = refresh.access_token
    access_token['email'] = voter.email

    return Response({
        "refresh": str(refresh),
        "access": str(access_token),
        "email": voter.email
    }, status=status.HTTP_200_OK)

voter_login.authentication_classes = []
voter_login.permission_classes = [AllowAny]

@csrf_exempt
@api_view(['POST'])
def register_voter(request):
    data = request.data.copy()
    if not data.get('email') or not data.get('password') or not data.get('name'):
        return Response({"error": "Name, email and password required"}, status=status.HTTP_400_BAD_REQUEST)

    if Voter.objects.filter(email=data['email']).exists():
        return Response({"error": "Email already registered"}, status=status.HTTP_400_BAD_REQUEST)

    data['password'] = make_password(data['password'])
    serializer = VoterSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response({
            "message": "Voter registered successfully!",
            "voter": serializer.data
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

register_voter.authentication_classes = []
register_voter.permission_classes = [AllowAny]

@csrf_exempt
@api_view(['POST'])
def vote(request):
    if not request.user.is_authenticated:
        return Response({"error": "Authentication required."}, status=status.HTTP_401_UNAUTHORIZED)

    user = request.user
    category_id = request.data.get("category_id")
    category_type = request.data.get("category_type")
    subcategory_id = request.data.get("subcategory_id")
    activity_id = request.data.get("activity_id")
    item_id = request.data.get("item_id") 

    if not category_id and not item_id and not category_type:
        return Response({"error": "Category and Item are required."}, status=status.HTTP_400_BAD_REQUEST)
    
    if category_id and subcategory_id:
        if category_type == "project":
            has_voted = Vote.objects.filter(voter=user, category__id=category_id, subcategory__id=subcategory_id, project__id=item_id).exists()

            if has_voted:
                return Response({"error": "You just voted for this category"},status=status.HTTP_400_BAD_REQUEST)
            
            else:
                Vote.objects.create(
                    voter=user,
                    activity_id=activity_id,
                    category_id=category_id,
                    subcategory_id=subcategory_id,
                    category_type=category_type,
                    project_id=item_id
                )
                return Response({"msg": "Voted with sucess"}, status=status.HTTP_200_OK)
            
        elif category_type == "member":
            has_voted = Vote.objects.filter(voter=user, category__id=category_id, subcategory__id=subcategory_id, member__id=item_id).exists()

            if has_voted:
                return Response({"error": "You just voted for this category"},status=status.HTTP_400_BAD_REQUEST)
            
            else:
                Vote.objects.create(
                    voter=user,
                    activity_id=activity_id,
                    category_id=category_id,
                    subcategory_id=subcategory_id,
                    category_type=category_type,
                    member_id=item_id
                )
                return Response({"msg": "Voted with sucess"}, status=status.HTTP_200_OK)
            
    elif category_id:
         if category_type == "members":
            has_voted = Vote.objects.filter(voter=user, category__id=category_id, member__id=item_id).exists()

            if has_voted:
                return Response({"error": "You just voted for this category"},status=status.HTTP_400_BAD_REQUEST)
            
            else:
                Vote.objects.create(
                    voter=user,
                    activity_id=activity_id,
                    category_id=category_id,
                    category_type=category_type,
                    member_id=item_id
                )

                return Response({"msg": "Voted with sucess"}, status=status.HTTP_200_OK)
            
         elif category_type == "stand":
            has_voted = Vote.objects.filter(voter=user, category__id=category_id, stand__id=item_id).exists()

            if has_voted:
                return Response({"error": "You just voted for this category"},status=status.HTTP_400_BAD_REQUEST)
            
            else:
                Vote.objects.create(
                    voter=user,
                    activity_id=activity_id,
                    category_id=category_id,
                    category_type=category_type,
                    stand_id=item_id
                )
                return Response({"msg": "Voted with sucess"}, status=status.HTTP_200_OK)

class VoterListView(APIView):
    def get(self, request):
        try:
            voters = Voter.objects.all()
            serializer = VoterSerializer(voters, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class RankingView(APIView):
    def get(self, request, activity_id):

        activites = Activity.objects.filter(id=activity_id).first()

        if not activites.finished:
            return Response({"msg": "Rank is not avaible now"}, status=status.HTTP_403_FORBIDDEN)
        
        rankings = generate_vote_ranking(activity_id)

        return Response(rankings, status=status.HTTP_200_OK)

class PublicRankingView(APIView):
    authentication_classes = []  
    permission_classes = []      

    def get(self, request, activity_id):
        activity = Activity.objects.filter(id=activity_id).first()

        if not activity:
            return Response({"error": "Activity not found"}, status=status.HTTP_404_NOT_FOUND)
        
        if not activity.finished:
            return Response({"msg": "Rank is not avaible now"}, status=status.HTTP_403_FORBIDDEN)
        rankings = generate_vote_ranking(activity_id)
        return Response(rankings, status=status.HTTP_200_OK)

class SubcategoryProjectRankingView(APIView):
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
