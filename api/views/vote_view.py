from api.models import Vote
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

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

    if not category_id and not item_id and not category_type:
        return Response({"error": "Category and Item are required."}, status=status.HTTP_400_BAD_REQUEST)
    
    if category_id and subcategory_id:
        if category_type == "project":
            has_voted = Vote.objects.filter(voter=user, category__id=category_id, subcategory__id=subcategory_id, project__id=item_id).exists()

            if has_voted:
                return Response({"error": "You just voted for this category"},status=status.HTTP_400_BAD_REQUEST)
            
            else:
                Vote.objects.create(
                    voter=user,
                    activity_id=activity_id,
                    category_id=category_id,
                    subcategory_id=subcategory_id,
                    category_type=category_type,
                    project_id=item_id
                )
                return Response({"msg": "Voted with sucess"}, status=status.HTTP_200_OK)
            
        elif category_type == "member":
            has_voted = Vote.objects.filter(voter=user, category__id=category_id, subcategory__id=subcategory_id, member__id=item_id).exists()

            if has_voted:
                return Response({"error": "You just voted for this category"},status=status.HTTP_400_BAD_REQUEST)
            
            else:
                Vote.objects.create(
                    voter=user,
                    activity_id=activity_id,
                    category_id=category_id,
                    subcategory_id=subcategory_id,
                    category_type=category_type,
                    member_id=item_id
                )
                return Response({"msg": "Voted with sucess"}, status=status.HTTP_200_OK)
            
    elif category_id:
         if category_type == "members":
            has_voted = Vote.objects.filter(voter=user, category__id=category_id, member__id=item_id).exists()

            if has_voted:
                return Response({"error": "You just voted for this category"},status=status.HTTP_400_BAD_REQUEST)
            
            else:
                Vote.objects.create(
                    voter=user,
                    activity_id=activity_id,
                    category_id=category_id,
                    category_type=category_type,
                    member_id=item_id
                )

                return Response({"msg": "Voted with sucess"}, status=status.HTTP_200_OK)
            
         elif category_type == "stand":
            has_voted = Vote.objects.filter(voter=user, category__id=category_id, stand__id=item_id).exists()

            if has_voted:
                return Response({"error": "You just voted for this category"},status=status.HTTP_400_BAD_REQUEST)
            
            else:
                Vote.objects.create(
                    voter=user,
                    activity_id=activity_id,
                    category_id=category_id,
                    category_type=category_type,
                    stand_id=item_id
                )
                return Response({"msg": "Voted with sucess"}, status=status.HTTP_200_OK)