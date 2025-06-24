from dal import autocomplete
from rest_framework import status
from django.db.models import Count
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import make_password, check_password
from api.models import Category, Project, Voter, Vote, Member, Activity
from api.serializers import ProjectSerializer, CategorySerializer, MemberSerializer, VoteSerializer, ActivitySerializer, VoterSerializer


# Create your views here.
class CategoryAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Category.objects.all()

        activity_id = self.forwarded.get('activity') or self.request.GET.get('activity')
        if activity_id:
            qs = qs.filter(activity_id=activity_id)

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

@api_view(['PUT'])
def update_activity(request, id):
    try:
        activity = Activity.objects.get(id=id)
    except Activity.DoesNotExist:
        return Response({"error": "Activity not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = ActivitySerializer(instance=activity, data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
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
def get_category(request, id):
    try:
        category = Category.objects.get(id=id)
    except Category.DoesNotExist:
        return Response({"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = CategorySerializer(category)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_members(request):
    members = Member.objects.all()
    serializer = MemberSerializer(members, many=True)
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

@csrf_exempt
@api_view(['POST'])
def vote_project(request):
    if not request.user.is_authenticated:
        return Response({"error": "Authentication required."}, status=status.HTTP_401_UNAUTHORIZED)

    voter = request.user
    
    category_id = request.data.get("category")
    project_id = request.data.get("project")

    if not category_id or not project_id:
        return Response({"error": "Category and Project are required."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        category = Category.objects.get(id=category_id)
    except Category.DoesNotExist:
        return Response({"error": "Category not found."}, status=status.HTTP_404_NOT_FOUND)

    try:
        project = Project.objects.get(id=project_id, category=category)
    except Project.DoesNotExist:
        return Response({"error": "Project not found in this category."}, status=status.HTTP_404_NOT_FOUND)

    if Vote.objects.filter(voter=voter, category=category, vote_type='project').exists():
        return Response({"error": "You have already voted in this category."}, status=status.HTTP_400_BAD_REQUEST)

    Vote.objects.create(
        voter=voter,
        category=category,
        project=project,
        vote_type='project'
    )

    return Response({"message": "Voted with success!"}, status=status.HTTP_201_CREATED)

@csrf_exempt
@api_view(['POST'])
def vote_expositor(request):
    voter = request.user

    category_id = request.data.get("category")
    member_id = request.data.get("member")

    if not category_id or not member_id:
        return Response({"error": "Category and member are required."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        category = Category.objects.get(id=category_id)
    except Category.DoesNotExist:
        return Response({"error": "Category not found."}, status=status.HTTP_404_NOT_FOUND)

    try:
        member = Member.objects.get(id=member_id)
    except Member.DoesNotExist:
        return Response({"error": "Member not found"}, status=status.HTTP_404_NOT_FOUND)

    if Vote.objects.filter(voter=voter, category=category, vote_type='expositor').exists():
        return Response({"error": "You have already voted a member in this category."}, status=status.HTTP_400_BAD_REQUEST)

    Vote.objects.create(
        voter=voter,
        category=category,
        member=member,
        vote_type='expositor'
    )

    return Response({"message": "Voted with success."}, status=status.HTTP_201_CREATED)

class ProjectRankingView(APIView):
    def get(self, request, category_id):

        category = Category.objects.get(id=category_id)

        projects = Project.objects.filter(category=category).annotate(vote_count=Count('vote')).order_by('-vote_count') 

        data = []
        for project in projects:
            data.append({
                'project_id': project.id,
                'name': project.name,
                'description': project.description,
                'category_name': category.name,
                'votes': project.vote_count
                
            })

        return Response(data)


class MemberRankingView(APIView):
    def get(self, request, category_id):

        category = Category.objects.get(id=category_id)

        projects = Project.objects.filter(category=category)

        members = Member.objects.filter(project__in=projects).annotate(vote_count=Count('vote')).order_by('-vote_count')

        data = []
        for member in members:
            data.append({
                'member_id': member.id,
                'name': member.name,
                'category_name': category.name,
                'votes': member.vote_count

            })

        return Response(data)