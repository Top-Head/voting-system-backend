from api import models
from rest_framework import status
from django.db.models import Count, Q
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


@cache_page(60 * 5)
@vary_on_cookie
@api_view(["GET"])
def get_projects(request):
    projects = Project.objects.all()
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


@cache_page(60 * 5)
@vary_on_cookie
@api_view(["GET"])
def get_categories_by_activity(request, activity_id):
    categories = Category.objects.filter(activity_id=activity_id)
    serializer = GetCategorySerializer(categories, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@cache_page(60 * 5)
@vary_on_cookie
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


@cache_page(60 * 5)
@vary_on_cookie
@api_view(["GET"])
def get_category_items(request):
    response = []
    category_id = int(request.GET.get("cat_id", 0))
    subcategory_id = int(request.GET.get("subcat_id", 0))
    category_type = request.GET.get("cat_tp", "")
    activity_id = int(request.GET.get("act_id", 0))

    print("get_category_items called", {
        "cat_id": category_id,
        "subcat_id": subcategory_id,
        "cat_tp": category_type,
        "act_id": activity_id,
    })

    if not request.user.is_authenticated:
        return Response(
            {"error": "Authentication required."}, status=status.HTTP_401_UNAUTHORIZED
        )

    user = request.user
    activity = Activity.objects.filter(id=activity_id).first()
    if not activity:
        print("get_category_items error: activity not found", activity_id)
        return Response(
            {"error": "Activity not found."}, status=status.HTTP_404_NOT_FOUND
        )

    category = Category.objects.filter(id=category_id, activity=activity).first()
    if not category:
        print("get_category_items error: category not found", category_id, activity_id)
        return Response(
            {"error": "Category not found for activity."},
            status=status.HTTP_404_NOT_FOUND,
        )

    subcategory = None
    if subcategory_id:
        subcategory = SubCategory.objects.filter(id=subcategory_id, category=category).first()
        if not subcategory:
            subcategories_in_cat = list(
                SubCategory.objects.filter(category=category).order_by("id")
            )
            if 1 <= subcategory_id <= len(subcategories_in_cat):
                subcategory = subcategories_in_cat[subcategory_id - 1]
                print(
                    "get_category_items notice: subcat_id interpreted as index, mapped",
                    subcategory_id,
                    "->",
                    subcategory.id,
                )
            else:
                print(
                    "get_category_items error: subcategory not found for category",
                    category_id,
                    subcategory_id,
                )
                return Response(
                    {"error": "Subcategory not found for this category."},
                    status=status.HTTP_404_NOT_FOUND,
                )

    def get_cover(value):
        if not value:
            return None
        if hasattr(value, "url"):
            try:
                return value.url
            except Exception as e:
                print("get_cover warning url failed", e)
        return str(value)

    try:
        if category_id and subcategory:
            if category_type == "project":
                projects = Project.objects.filter(
                    subcategory=subcategory, activity__id=activity.id
                )

                for proj in projects:
                    has_voted = Vote.objects.filter(
                        voter=user,
                        category__id=category_id,
                        subcategory=subcategory,
                        project=proj,
                        activity__id=activity.id,
                    ).exists()
                    response.append(
                        {
                            "id": proj.id,
                            "name": proj.name or "",
                            "cover": get_cover(proj.project_cover),
                            "activity": proj.activity.name if proj.activity else "",
                            "classe": None,
                            "turma": None,
                            "course": None,
                            "has_voted": has_voted,
                        }
                    )

            elif category_type in ["member", "members"]:
                if subcategory:
                    members = Member.objects.filter(
                        subcategory=subcategory, activity__id=activity.id
                    )
                else:
                    members = Member.objects.filter(
                        category=category, activity__id=activity.id
                    )

                for member in members:
                    has_voted = Vote.objects.filter(
                        voter=user,
                        category__id=category_id,
                        subcategory=subcategory, 
                        member=member,
                        activity__id=activity.id,
                    ).exists()
                    response.append(
                        {
                            "id": member.id,
                            "name": member.name or "",
                            "cover": get_cover(member.profile_image),
                            "classe": member.classe or "",
                            "turma": member.turma or "",
                            "course": member.course or "",
                            "activity": member.activity.name if member.activity else "",
                            "type": category_type,
                            "has_voted": has_voted,
                        }
                    )

            return Response({"data": response}, status=status.HTTP_200_OK)

        elif category_id:
            if category_type in ["member", "members"]:
                members = Member.objects.filter(
                    category__id=category_id, activity__id=activity.id
                )

                for member in members:
                    has_voted = Vote.objects.filter(
                        voter=user,
                        category__id=category_id,
                        member=member,
                        activity__id=activity.id,
                    ).exists()
                    response.append(
                        {
                            "id": member.id,
                            "name": member.name or "",
                            "cover": get_cover(member.profile_image),
                            "classe": member.classe or "",
                            "turma": member.turma or "",
                            "course": member.course or "",
                            "activity": member.activity.name if member.activity else "",
                            "type": category_type,
                            "has_voted": has_voted,
                        }
                    )

            elif category_type == "stand":
                stands = Stand.objects.filter(
                    category__id=category_id, activity__id=activity.id
                )

                for stand in stands:
                    has_voted = Vote.objects.filter(
                        voter=user,
                        category__id=category_id,
                        stand=stand,
                        activity__id=activity.id,
                    ).exists()
                    response.append(
                        {
                            "id": stand.id,
                            "name": stand.name or "",
                            "cover": get_cover(stand.stand_cover),
                            "activity": stand.activity.name if stand.activity else "",
                            "type": category_type,
                            "classe": None,
                            "turma": None,
                            "course": None,
                            "has_voted": has_voted,
                        }
                    )

            elif category_type == "project":
                projects = Project.objects.filter(
                    category__id=category_id, activity__id=activity.id
                )

                for proj in projects:
                    has_voted = Vote.objects.filter(
                        voter=user,
                        category__id=category_id,
                        project=proj,
                        activity__id=activity.id,
                    ).exists()
                    response.append(
                        {
                            "id": proj.id,
                            "name": proj.name or "",
                            "cover": get_cover(proj.project_cover),
                            "activity": proj.activity.name if proj.activity else "",
                            "classe": None,
                            "turma": None,
                            "course": None,
                            "has_voted": has_voted,
                        }
                    )

            return Response({"data": response}, status=status.HTTP_200_OK)

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
    members = Member.objects.all()
    serializer = GetMemberSerializer(members, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@cache_page(60 * 5)
@vary_on_cookie
@api_view(["GET"])
def get_member(request, member_id):
    try:
        member = Member.objects.filter(id=member_id)
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

    members = Member.objects.filter(project__category=category)
    serializer = GetMemberSerializer(members, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@cache_page(60 * 5)
@vary_on_cookie
@api_view(["GET"])
def get_votes(request):
    votes = Vote.objects.all()
    serializer = VoteSerializer(votes, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@cache_page(60 * 5)
@vary_on_cookie
@api_view(["GET"])
def get_activities(request):
    activitys = Activity.objects.all()
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
