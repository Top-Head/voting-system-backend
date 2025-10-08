from dal import autocomplete
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from api.models import Category, Project, Activity, SubCategory, Stand
from api.services.cloudinary import upload_to_cloudinary_projects, upload_to_cloudinary_members, upload_to_cloudinary_stand
from api.serializers import ProjectSerializer, ActivitySerializer, SubCategorySerializer, CategorySerializer, MemberSerializer, StandSerializer

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

class ProjectAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Project.objects.all()
        
        subcategory_id = self.forwarded.get('subcategory') or self.request.GET.get('subcategory')
        if subcategory_id:
            qs = qs.filter(subcategory_id=subcategory_id)
            
        if self.q:
            qs = qs.filter(name__icontains=self.q)
            
        return qs


@api_view(['POST'])
def create_activity(request):
    serializer = ActivitySerializer(data=request.data)
    if serializer.is_valid():
        activity = serializer.save()
        return Response({"message": "Atividade criada com sucesso!", "activity": ActivitySerializer(activity).data}, status=201)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def update_activity(request, activity_id):
    try:
        activity = Activity.objects.get(id=activity_id)
    except Activity.DoesNotExist:
        return Response({"error": "Activity not found"}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = Activity(instance=activity, data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)

@api_view(['PATCH'])
def close_activity(request, activity_id):
    try:
        activity = Activity.objects.get(id=activity_id)
    except Activity.DoesNotExist:
        return Response({"error": "Activity not found"}, status=status.HTTP_404_NOT_FOUND)
    
    if activity.finished == False:
        activity.finished = True
        activity.save()
        return Response({"message": "Activity closed successfully"}, status=status.HTTP_200_OK)
    
    else:
        activity.finished = False
        activity.save()
        return Response({"message": "Activity opened sucessfullt"}, status=status.HTTP_200_OK)
    
@api_view(['DELETE'])
def delete_activity(request, activity_id):
    try:
        activity = Activity.objects.get(id=activity_id)
    except Activity.DoesNotExist:
        return Response({"error": "Activity not found"}, status=status.HTTP_404_NOT_FOUND)
    
    activity.delete()

    return Response({"message": "Activity deleted with sucess"}, status=status.HTTP_200_OK)

@api_view(['POST'])
def create_category(request):
    serializer = CategorySerializer(data=request.data)
    if serializer.is_valid():
        category = serializer.save()
        return Response({"message": "Categoria criada com sucesso!", "category": CategorySerializer(category).data}, status=201)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_category(request, category_id):
    try:
        category = Category.objects.get(id=category_id)
    except Activity.DoesNotExist:
        return Response({"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND)
    
    category.delete()

    return Response({"message": "Category deleted with sucess"}, status=status.HTTP_200_OK)

@api_view(['POST'])
def create_subcategory(request):
    serializer = SubCategorySerializer(data=request.data)
    if serializer.is_valid():
        subcategory = serializer.save()
        return Response({"message": "Subcategoria criada com sucesso!", "subcategory": SubCategorySerializer(subcategory).data}, status=201)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_subcategory(request, subcategory_id):
    try:
        subcategory = SubCategory.objects.get(id=subcategory_id)
    except SubCategory.DoesNotExist:
        return Response({"error": "Activity not found"}, status=status.HTTP_404_NOT_FOUND)
    
    subcategory.delete()

    return Response({"message": "Activity deleted with sucess"}, status=status.HTTP_200_OK)

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
def update_project(request, project_id):
    try:
        project = Project.objects.get(id=project_id)
    except Project.DoesNotExist:
        return Response({"error": "Project not found"}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = ProjectSerializer(instance=project, data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)

@api_view(['DELETE'])
def delete_project(request, project_id):
    try:
        project = Project.objects.get(id=project_id)
    except Project.DoesNotExist:
        return Response({"error": "Activity not found"}, status=status.HTTP_404_NOT_FOUND)
    
    project.delete()

    return Response({"message": "Project deleted with sucess"}, status=status.HTTP_200_OK)

@api_view(['POST'])
def create_stand(request):
    if "stand_cover" not in request.FILES:
        return Response({"error": "Image is required"}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        image_file = request.FILES['stand_cover'] 
        image_url = upload_to_cloudinary_stand(image_file)

        data = request.data.copy()
        data['stand_cover'] = image_url

        serializer = StandSerializer(data=data)

        if serializer.is_valid():
            stand = serializer.save()
            return Response({"message": "Stand criado com sucesso!", "stand": StandSerializer(stand).data}, status=status.HTTP_201_CREATED)
    
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['DELETE'])
def delete_stand(request, stand_id):
    try:
        stand = Stand.objects.get(id=stand_id)
    except Stand.DoesNotExist:
        return Response({"error": "Activity not found"}, status=status.HTTP_404_NOT_FOUND)
    
    stand.delete()

    return Response({"message": "Activity deleted with sucess"}, status=status.HTTP_200_OK)

@api_view(['POST'])
def create_member(request):
    if "profile_image" not in request.FILES:
        return Response({"error": "Image is required"}, status=status.HTTP_400_BAD_REQUEST)
    try:
        image_file = request.FILES['profile_image'] 
        image_url = upload_to_cloudinary_members(image_file)

        data = request.data.copy()
        data['profile_image'] = image_url

        serializer = MemberSerializer(data=data)

        if serializer.is_valid():
            member = serializer.save()
            return Response({"message": "Membro criado com sucesso!", "member": MemberSerializer(member).data}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)