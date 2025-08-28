from dal import autocomplete
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from api.models import Category, Project, Activity, SubCategory
from api.services.cloudinary import upload_to_cloudinary_projects
from api.serializers import ProjectSerializer, ActivitySerializer, SubCategorySerializer

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
    if 'project_cover' not in request.FILES:
        return Response({"error": "Image is required"}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        image_file = request.FILES['project_cover']
        image_url = upload_to_cloudinary_projects(image_file)
        
        data = request.data.copy()
        data['project_cover'] = image_url
        
        serializer = ProjectSerializer(data=data)
        
        if serializer.is_valid():
            project = serializer.save()
            return Response({
                "message": "Projeto criado com sucesso!",
                "project": ProjectSerializer(project).data
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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