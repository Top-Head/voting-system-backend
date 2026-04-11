from django.shortcuts import get_object_or_404
from django.core.cache import cache
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from api.models import Project, Member, Stand, Vote, Activity

def invalidate_vote_cache(activity_id=None, user_id=None):
    """
    Priority 2: Cache invalidation helper
    Invalida cache quando votos são criados/atualizados
    """
    if activity_id:
        cache.delete(f'ranking:{activity_id}')
        cache.delete(f'ranking_public:{activity_id}')
    if user_id:
        cache.delete(f'user_votes:{user_id}')

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
        project = get_object_or_404(Project.objects.select_related('subcategory', 'activity'), id=item_id)
        
        has_voted = Vote.objects.filter(
            voter=user, 
            project__subcategory_id=project.subcategory_id
        ).exists()

        if has_voted:
            return Response({"error": "Já votaste num projeto deste curso!"}, status=status.HTTP_400_BAD_REQUEST)

        Vote.objects.create(voter=user, project=project)
        # Priority 2: Cache invalidation
        invalidate_vote_cache(activity_id=project.activity_id, user_id=user.id)

    # --- LÓGICA PARA MEMBROS (Expositores) ---
    elif category_type in ["member", "members"]:
        member = get_object_or_404(Member.objects.select_related('project__subcategory', 'activity'), id=item_id)
        
        has_voted = Vote.objects.filter(
            voter=user, 
            member__project__subcategory_id=member.project.subcategory_id
        ).exists()

        if has_voted:
            return Response({"error": "Já votaste num expositor deste curso!"}, status=status.HTTP_400_BAD_REQUEST)

        Vote.objects.create(voter=user, member=member)
        # Priority 2: Cache invalidation
        invalidate_vote_cache(activity_id=member.activity_id, user_id=user.id)

    # --- LÓGICA PARA STANDS ---
    elif category_type == "stand":
        stand = get_object_or_404(Stand.objects.select_related('category', 'activity'), id=item_id)
        
        has_voted = Vote.objects.filter(
            voter=user, 
            stand__category_id=stand.category_id
        ).exists()

        if has_voted:
            return Response({"error": "Já votaste num stand desta categoria!"}, status=status.HTTP_400_BAD_REQUEST)

        Vote.objects.create(voter=user, stand=stand)
        # Priority 2: Cache invalidation
        invalidate_vote_cache(activity_id=stand.activity_id, user_id=user.id)

    else:
        return Response({"error": "Invalid category type."}, status=status.HTTP_400_BAD_REQUEST)

    return Response({"msg": "Voto registado com sucesso!"}, status=status.HTTP_200_OK)