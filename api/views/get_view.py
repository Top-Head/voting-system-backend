from rest_framework import status
from django.db.models import Count, Q
from rest_framework.pagination import PageNumberPagination 
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from rest_framework.decorators import api_view, permission_classes
from api.models import Category, Project, Vote, Member, Activity, SubCategory, Stand
from api.serializers import (
    GetActivitySerializer,
    GetCategorySerializer,
    GetMemberSerializer,
    GetProjectSerializer,
    GetSubCategorySerializer,
    VoterSerializer,
    VoteSerializer,
)


@cache_page(60 * 5)
@vary_on_cookie
@api_view(["GET"])
def count_project(request):
    project_count = Project.objects.count()
    return Response({"total": project_count}, status=status.HTTP_200_OK)


@cache_page(60 * 5)
@vary_on_cookie
@api_view(["GET"])
def count_voters(self):
    member_count = Member.objects.count()
    return Response({"total": member_count}, status=status.HTTP_200_OK)


@cache_page(60 * 5)
@vary_on_cookie
@api_view(["GET"])
def count_activity(request):
    activity_count = Activity.objects.count()
    return Response({"total": activity_count}, status=status.HTTP_200_OK)


@cache_page(60 * 5)
@vary_on_cookie
@api_view(["GET"])
def count_members(request):
    member_count = Member.objects.count()
    return Response({"total": member_count}, status=status.HTTP_200_OK)


@cache_page(60 * 5)
@vary_on_cookie
@api_view(["GET"])
def count_project_in_category(request, activity_id):
    try:
        activity = Activity.objects.get(id=activity_id)
    except Activity.DoesNotExist:
        return Response(
            {"error": "Activity does not exist"}, status=status.HTTP_404_NOT_FOUND
        )

    category_count = (
        Category.objects.filter(activity_id=activity)
        .annotate(project_count=Count("projects"))
        .values("name", "project_count")
    )
    return Response({"Total": list(category_count)}, status=status.HTTP_200_OK)


@cache_page(60 * 5)
@vary_on_cookie
@api_view(["GET"])
def activity_project_count(request, activity_id):
    try:
        activity = (
            Activity.objects.filter(id=activity_id)
            .annotate(project_count=Count("projects"))
            .values("project_count")
            .first()
        )

        if not activity:
            return Response({"error": "Activity not found"}, status=404)

        return Response(activity, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(["GET"])
def get_projects(request):
    projects = (
        Project.objects
        .select_related('activity', 'category', 'subcategory')
        .prefetch_related('members')
        .all()
    )
    serializer = GetProjectSerializer(projects, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@cache_page(60 * 5)
@vary_on_cookie
@api_view(["GET"])
def get_project(request, project_id):
    try:
        project = Project.objects.get(id=project_id)
    except Project.DoesNotExist:
        return Response(
            {"error": "Project not found"}, status=status.HTTP_404_NOT_FOUND
        )

    serializer = GetProjectSerializer(project)
    return Response(serializer.data, status=status.HTTP_200_OK)



@api_view(["GET"])
def get_categories_by_activity(request, activity_id):
    categories = Category.objects.filter(activity_id=activity_id)
    serializer = GetCategorySerializer(categories, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)



@api_view(["GET"])
def get_category(request, category_id):
    try:
        category = Category.objects.get(id=category_id)
    except Category.DoesNotExist:
        return Response(
            {"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND
        )

    serializer = GetCategorySerializer(category)
    return Response(serializer.data, status=status.HTTP_200_OK)



@api_view(["GET"])
def get_category_items(request):
    response = []
    category_id = int(request.GET.get("cat_id", 0))
    subcategory_id = int(request.GET.get("subcat_id", 0))
    category_type = request.GET.get("cat_tp", "")
    activity_id = int(request.GET.get("act_id", 0))

    if not request.user.is_authenticated:
        return Response({"error": "Authentication required."}, status=status.HTTP_401_UNAUTHORIZED)

    user = request.user

    activity = Activity.objects.filter(id=activity_id).first()
    if not activity:
        return Response({"error": "Activity not found."}, status=status.HTTP_404_NOT_FOUND)

    category = Category.objects.filter(id=category_id, activity=activity).first()
    if not category:
        return Response({"error": "Category not found for activity."}, status=status.HTTP_404_NOT_FOUND)

    subcategory = None
    if subcategory_id:
        subcategory = SubCategory.objects.filter(id=subcategory_id, category=category).first()
        if not subcategory:
            return Response({"error": "Subcategory not found for this category."}, status=status.HTTP_404_NOT_FOUND)

    def get_cover(value):
        if not value:
            return None

        try:
            clean = str(value).split("||")[0].strip() 
            return clean if clean else None

        except Exception:
            return None
        
    try:
        if category_type == "project":
            qs = Project.objects.filter(activity=activity, category=category)
            if subcategory:
                qs = qs.filter(subcategory=subcategory)

            user_voted_project_ids = set(
                Vote.objects.filter(voter=user, project_id__in=qs.values_list('id', flat=True))
                .values_list('project_id', flat=True)
            )

            for proj in qs:
                response.append({
                    "id": proj.id,
                    "name": proj.name or "",
                    "cover": get_cover(proj.project_cover),
                    "activity": activity.name,
                    "type": category_type,
                    "has_voted": proj.id in user_voted_project_ids,
                })

        elif category_type in ["member", "members"]:
            if subcategory:
                qs = Member.objects.select_related('project').filter(
                    activity=activity,
                    project__subcategory__name=subcategory.name
                )
            else:
                qs = Member.objects.select_related('project').filter(activity=activity)

            user_voted_member_ids = set(
                Vote.objects.filter(voter=user, member_id__in=qs.values_list('id', flat=True))
                .values_list('member_id', flat=True)
            )

            for member in qs:
                response.append({
                    "id": member.id,
                    "name": member.name or "",
                    "cover": get_cover(member.profile_image),
                    "classe": member.classe or "",
                    "turma": member.turma or "",
                    "course": member.course or "",
                    "activity": activity.name,
                    "project": member.project.name if member.project else "",
                    "type": category_type,
                    "has_voted": member.id in user_voted_member_ids,
                })

        elif category_type == "stand":
            qs = Stand.objects.filter(activity=activity, category=category)
            if subcategory:
                qs = qs.filter(subcategory=subcategory)

            user_voted_stand_ids = set(
                Vote.objects.filter(voter=user, stand_id__in=qs.values_list('id', flat=True))
                .values_list('stand_id', flat=True)
            )

            for stand in qs:
                response.append({
                    "id": stand.id,
                    "name": stand.name or "",
                    "cover": get_cover(stand.stand_cover),
                    "activity": activity.name,
                    "type": category_type,
                    "has_voted": stand.id in user_voted_stand_ids,
                })

        return Response({"data": response}, status=status.HTTP_200_OK)

    except Exception as e:
        print("get_category_items failed", str(e))
        return Response(
            {"error": "Internal Server Error", "details": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

@cache_page(60 * 5)
@vary_on_cookie
@api_view(["GET"])
def get_members(request):
    members = Member.objects.select_related('activity', 'project').all()
    serializer = GetMemberSerializer(members, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@cache_page(60 * 5)
@vary_on_cookie
@api_view(["GET"])
def get_member(request, member_id):
    try:
        member = Member.objects.select_related('activity', 'project').filter(id=member_id)
    except Member.DoesNotExist:
        return Response({"error": "Member not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = GetMemberSerializer(member)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_me(request):
    serializer = VoterSerializer(request.user)
    return Response(serializer.data)


@cache_page(60 * 5)
@vary_on_cookie
@api_view(["GET"])
def get_subcategories(request, category_id, activity_id):
    try:
        subcategories = SubCategory.objects.filter(
            category_id=category_id,
            activity_id=activity_id
        )
        if not subcategories.exists():
            return Response(
                {"message": "Nenhuma subcategoria encontrada"},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = GetSubCategorySerializer(subcategories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@cache_page(60 * 5)
@vary_on_cookie
@api_view(["GET"])
def get_subcategory(request, id):
    try:
        subcategory = SubCategory.objects.get(id=id)
    except SubCategory.DoesNotExist:
        return Response(
            {"error": "Subcategory not found"}, status=status.HTTP_404_NOT_FOUND
        )

    serializer = GetSubCategorySerializer(subcategory)
    return Response(serializer.data, status=status.HTTP_200_OK)


@cache_page(60 * 5)
@vary_on_cookie
@api_view(["GET"])
def get_members_by_category(request, category_id):
    try:
        category = Category.objects.get(id=category_id)
    except Category.DoesNotExist:
        return Response(
            {"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND
        )

    members = Member.objects.select_related('project').filter(project__category=category)
    serializer = GetMemberSerializer(members, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@cache_page(60 * 5)
@vary_on_cookie
@api_view(["GET"])
def get_votes(request):
    votes = Vote.objects.select_related('voter', 'project', 'member', 'stand').all()
    serializer = VoteSerializer(votes, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@cache_page(60 * 5)
@vary_on_cookie
@api_view(["GET"])
def get_activities(request):
    activitys = (
        Activity.objects
        .prefetch_related('categories', 'projects', 'members', 'subcategories')
        .all()
    )
    serializer = GetActivitySerializer(activitys, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@cache_page(60 * 5)
@vary_on_cookie
@api_view(["GET"])
def get_activity(request, activity_id):
    try:
        activity = Activity.objects.get(id=activity_id)
    except Activity.DoesNotExist:
        return Response(
            {"error": "Activity not found"}, status=status.HTTP_404_NOT_FOUND
        )

    serializer = GetActivitySerializer(activity)
    return Response(serializer.data, status=status.HTTP_200_OK)


@cache_page(60)
@vary_on_cookie
@api_view(["GET"])
def top_projects(request):
    projects = Project.objects.annotate(
        vote_count=Count("vote", filter=Q(vote__project__isnull=False))
    ).order_by("-vote_count")[:5]

    data = [
        {"name": project.name, "vote_count": project.vote_count} for project in projects
    ]

    return Response(data, status=status.HTTP_200_OK)


@api_view(["GET"])
def get_members_by_subcategory(request, subcategory_id):
    try:
        members = Member.objects.filter(subcategory_id=subcategory_id)
        if not members.exists():
            return Response(
                {"message": "Nenhum membro encontrado para esta subcategoria."},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = GetMemberSerializer(members, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    except Exception as e:
        return Response(
            {"error": f"Erro ao buscar membros: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
