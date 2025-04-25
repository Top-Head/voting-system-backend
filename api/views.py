from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny, IsAdminUser
from api.serializers import ProjectSerializer, CategorySerializer
from rest_framework.decorators import api_view, permission_classes

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
    
@api_view(['POST'])
@permission_classes([IsAdminUser]) 
def create_project_with_members(request):
    serializer = ProjectSerializer(data=request.data)

    if serializer.is_valid():
        project = serializer.save()
        return Response({
            "message": "Projeto criado com sucesso!",
            "project": ProjectSerializer(project).data
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)














#---------------------------------------------Voter-------------------------------------------------