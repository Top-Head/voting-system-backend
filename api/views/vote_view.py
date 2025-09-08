from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from api.models import Vote, Project, Member, Stand

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

    if not category_id or not item_id or not category_type:
        return Response({"error": "Category, type and item are required."}, status=status.HTTP_400_BAD_REQUEST)

    # --- Project ---
    if category_type == "project" and subcategory_id:
        project = get_object_or_404(Project, id=item_id)

        has_voted = Vote.objects.filter(
            voter=user, category_id=category_id, subcategory_id=subcategory_id, project=project
        ).exists()

        if has_voted:
            return Response({"error": "You already voted in this category."}, status=status.HTTP_400_BAD_REQUEST)

        Vote.objects.create(
            voter=user,
            activity_id=activity_id,
            category_id=category_id,
            subcategory_id=subcategory_id,
            category_type=category_type,
            project=project
        )
        return Response({"msg": "Voted successfully"}, status=status.HTTP_200_OK)

    # --- Member ---
    elif category_type == "member" and subcategory_id:
        member = get_object_or_404(Member, id=item_id)

        has_voted = Vote.objects.filter(
            voter=user, category_id=category_id, subcategory_id=subcategory_id, member=member
        ).exists()

        if has_voted:
            return Response({"error": "You already voted in this category."}, status=status.HTTP_400_BAD_REQUEST)

        Vote.objects.create(
            voter=user,
            activity_id=activity_id,
            category_id=category_id,
            subcategory_id=subcategory_id,
            category_type=category_type,
            member=member
        )
        return Response({"msg": "Voted successfully"}, status=status.HTTP_200_OK)

    # --- Member (sem subcategory) ---
    elif category_type == "members":
        member = get_object_or_404(Member, id=item_id)

        has_voted = Vote.objects.filter(
            voter=user, category_id=category_id, member=member
        ).exists()

        if has_voted:
            return Response({"error": "You already voted in this category."}, status=status.HTTP_400_BAD_REQUEST)

        Vote.objects.create(
            voter=user,
            activity_id=activity_id,
            category_id=category_id,
            category_type=category_type,
            member=member
        )
        return Response({"msg": "Voted successfully"}, status=status.HTTP_200_OK)

    # --- Stand ---
    elif category_type == "stand":
        stand = get_object_or_404(Stand, id=item_id)

        has_voted = Vote.objects.filter(
            voter=user, category_id=category_id, stand=stand
        ).exists()

        if has_voted:
            return Response({"error": "You already voted in this category."}, status=status.HTTP_400_BAD_REQUEST)

        Vote.objects.create(
            voter=user,
            activity_id=activity_id,
            category_id=category_id,
            category_type=category_type,
            stand=stand
        )
        return Response({"msg": "Voted successfully"}, status=status.HTTP_200_OK)

    return Response({"error": "Invalid category_type or missing subcategory."}, status=status.HTTP_400_BAD_REQUEST)
