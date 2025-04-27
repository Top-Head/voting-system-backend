from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.db.models import Count
from api.models import Category, Project, Voter, Vote, Member
from api.serializers import ProjectSerializer, CategorySerializer, MemberSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated

# Create your views here.
# ---------------------------------------------Admin-----------------------------------------------  

ADMIN_CODE = 'CODE'


@api_view(['POST'])
@permission_classes([AllowAny])
def admin_login(request):
    email = request.data.get("email")
    password = request.data.get("password")
    secret_code = request.data.get("secret_code")

    if secret_code != ADMIN_CODE:
        return Response({"error": "Invalid secret code"}, status=status.HTTP_401_UNAUTHORIZED)

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({"error": "Invalid email"}, status=status.HTTP_404_NOT_FOUND)

    user = authenticate(request, username=user.username, password=password)
    if user is None:
        return Response({"error": "Invalid password"}, status=status.HTTP_401_UNAUTHORIZED)

    if not user.is_superuser:
        return Response({"error": "Not a superuser"}, status=status.HTTP_403_FORBIDDEN)

    refresh = RefreshToken.for_user(user)

    return Response({
        "refresh": str(refresh),
        "access": str(refresh.access_token),
        "email": user.email
    }, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAdminUser])
def create_category(request):
    serializer = CategorySerializer(data=request.data)
    
    if serializer.is_valid():
        category = serializer.save()
        return Response({
            "message": "Categoria criada com sucesso!",
            "category": CategorySerializer(category).data
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([IsAdminUser])
def update_category(request, id):
    try:
        category = Category.objects.get(id=id)
    except Category.DoesNotExist:
        return Response({"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = CategorySerializer(instance=category, data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PATCH'])
@permission_classes([IsAdminUser])
def close_category(request, id):
    try:
        category = Category.objects.get(id=id)
    except Category.DoesNotExist:
        return Response({"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND)

    category.finished = True
    category.save()

    return Response({"message": "Category closed successfully"}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAdminUser]) 
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
@permission_classes([IsAdminUser])
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

#------------------------------------------------------------------------------------------------------

@api_view(['GET'])
def count_project(request):
    project_count = Project.objects.count()
    return Response({"total": project_count}, status=status.HTTP_200_OK)

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

#---------------------------------------------Voter-------------------------------------------------
@api_view(['POST'])
@permission_classes([AllowAny])  
def voter_login(request):

    email = request.data.get('email')
    google_id = request.data.get('google_id')

    if not email or not google_id:
        return Response({"error": "Email and Google ID required"}, status=status.HTTP_400_BAD_REQUEST)

    voter, created = Voter.objects.get_or_create(
        google_id=google_id,
        defaults={"email": email}
    )

    if not created and voter.email != email:
        voter.email = email
        voter.save()

    refresh = RefreshToken.for_user(voter)

    return Response({
        "refresh": str(refresh),
        "access": str(refresh.access_token),
        "email": voter.email
    }, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def vote_project(request):
    voter = request.user
    category_id = request.data.get("category")
    project_id = request.data.get("project")

    if not category_id or not project_id:
        return Response({"error": "Category and Project are required."}, status=status.HTTP_400_BAD_REQUEST)

    if Vote.objects.filter(voter=voter, category_id=category_id, vote_type='project').exists():
        return Response({"error": "You just voted in this category."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        project = Project.objects.get(id=project_id)
    except Project.DoesNotExist:
        return Response({"error": "Project not found."}, status=status.HTTP_404_NOT_FOUND)

    Vote.objects.create(
        voter=voter,
        category_id=category_id,
        project=project,
        vote_type='project'
    )

    return Response({"message": "Voted with sucess!"}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def vote_expositor(request):
    voter = request.user
    category_id = request.data.get("category")
    member_id = request.data.get("member")

    if not category_id or not member_id:
        return Response({"error": "Category and members are required."}, status=status.HTTP_400_BAD_REQUEST)

    if Vote.objects.filter(voter=voter, category_id=category_id, vote_type='expositor').exists():
        return Response({"error": "You just voted a member"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        member = Member.objects.get(id=member_id)
    except Member.DoesNotExist:
        return Response({"error": "Member not found"}, status=status.HTTP_404_NOT_FOUND)

    Vote.objects.create(
        voter=voter,
        category_id=category_id,
        member=member,
        vote_type='expositor'
    )

    return Response({"message": "Voted with sucess."}, status=status.HTTP_201_CREATED)

class ProjectRankingView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, category_id):

        category = Category.objects.get(id=category_id)

        projects = Project.objects.filter(category=category).annotate(vote_count=Count('vote')).order_by('-vote_count') 

        data = []
        for project in projects:
            data.append({
                'project_id': project.id,
                'name': project.name,
                'description': project.description,
                'votes': project.vote_count
            })

        return Response(data)


class MemberRankingView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, category_id):

        category = Category.objects.get(id=category_id)

        projects = Project.objects.filter(category=category)

        members = Member.objects.filter(project__in=projects).annotate(vote_count=Count('vote')).order_by('-vote_count')

        data = []
        for member in members:
            data.append({
                'member_id': member.id,
                'name': member.name,
                'votes': member.vote_count
            })

        return Response(data)