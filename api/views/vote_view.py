from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from api.models import Project, Member, Stand, Vote

@api_view(["POST"])
def vote(request):
    if not request.user.is_authenticated:
        return Response({"error": "Authentication required."}, status=status.HTTP_401_UNAUTHORIZED)

    user = request.user
    category_type = request.data.get("category_type")
    item_id = request.data.get("item_id")

    if not item_id or not category_type:
        return Response({"error": "Item ID and category type are required."}, status=status.HTTP_400_BAD_REQUEST)

    # --- LÓGICA PARA PROJETOS ---
    if category_type == "project":
        project = get_object_or_404(Project, id=item_id)
        
        has_voted = Vote.objects.filter(
            voter=user, 
            project__subcategory=project.subcategory
        ).exists()

        if has_voted:
            return Response({"error": "Já votaste num projeto deste curso!"}, status=status.HTTP_400_BAD_REQUEST)

        Vote.objects.create(voter=user, project=project)

    # --- LÓGICA PARA MEMBROS (Expositores) ---
    elif category_type in ["member", "members"]:
        member = get_object_or_404(Member, id=item_id)
        
        has_voted = Vote.objects.filter(
            voter=user, 
            member__project__subcategory=member.project.subcategory
        ).exists()

        if has_voted:
            return Response({"error": "Já votaste num expositor deste curso!"}, status=status.HTTP_400_BAD_REQUEST)

        Vote.objects.create(voter=user, member=member)

    # --- LÓGICA PARA STANDS ---
    elif category_type == "stand":
        stand = get_object_or_404(Stand, id=item_id)
        
        has_voted = Vote.objects.filter(
            voter=user, 
            stand__category=stand.category
        ).exists()

        if has_voted:
            return Response({"error": "Já votaste num stand desta categoria!"}, status=status.HTTP_400_BAD_REQUEST)

        Vote.objects.create(voter=user, stand=stand)

    else:
        return Response({"error": "Invalid category type."}, status=status.HTTP_400_BAD_REQUEST)

    return Response({"msg": "Voto registado com sucesso!"}, status=status.HTTP_200_OK)