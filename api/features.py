from django.db.models import Count, F, Value, Q
from django.db.models import CharField
from api.models import Vote


def generate_vote_ranking(activity_id):
    results = []

    activity_votes = Vote.objects.filter(
        Q(project__activity=activity_id) | Q(member__activity=activity_id) | Q(stand__activity=activity_id)
    )

    vote_targets = ["stand", "member", "project"]

    for target in vote_targets:
        votes = activity_votes.filter(**{f"{target}__isnull": False})

        if target == "stand":
            common_values = {
                "alias_cat_id": F("stand__category__id"),
                "alias_cat_name": F("stand__category__name"),
                "alias_cat_type": F("stand__category__category_type"),
                "alias_subcat_id": Value(None, output_field=CharField()),
                "alias_subcat_name": Value(None, output_field=CharField()),
            }
            votes = votes.values(
                "stand__id",
                "stand__name",
                "stand__stand_cover",
                **common_values,
            ).annotate(
                id=F("stand__id"),
                name=F("stand__name"),
                cover=F("stand__stand_cover"),
                profile_image=Value(None, output_field=CharField()),
                grade=Value(None, output_field=CharField()),
                group=Value(None, output_field=CharField()),
                course=Value(None, output_field=CharField()),
                alias_total_votes=Count("id"),
            )

        elif target == "member":
            common_values = {
                "alias_cat_id": F("member__project__category__id"),
                "alias_cat_name": F("member__project__category__name"),
                "alias_cat_type": F("member__project__category__category_type"),
                "alias_subcat_id": F("member__project__subcategory__id"),
                "alias_subcat_name": F("member__project__subcategory__name"),
            }
            votes = votes.values(
                "member__id",
                "member__name",
                "member__profile_image",
                "member__classe",
                "member__turma",
                "member__course",
                **common_values,
            ).annotate(
                id=F("member__id"),
                name=F("member__name"),
                cover=Value(None, output_field=CharField()),
                profile_image=F("member__profile_image"),
                grade=F("member__classe"),
                group=F("member__turma"),
                course=F("member__course"),
                alias_total_votes=Count("id"),
            )

        elif target == "project":
            common_values = {
                "alias_cat_id": F("project__category__id"),
                "alias_cat_name": F("project__category__name"),
                "alias_cat_type": F("project__category__category_type"),
                "alias_subcat_id": F("project__subcategory__id"),
                "alias_subcat_name": F("project__subcategory__name"),
            }
            votes = votes.values(
                "project__id",
                "project__name",
                **common_values,
            ).annotate(
                id=F("project__id"),
                name=F("project__name"),
                cover=Value(None, output_field=CharField()),
                profile_image=Value(None, output_field=CharField()),
                grade=Value(None, output_field=CharField()),
                group=Value(None, output_field=CharField()),
                course=Value(None, output_field=CharField()),
                alias_total_votes=Count("id"),
            )

        grouped = {}
        for vote in votes:
            key = (
                vote["alias_cat_id"],
                vote["alias_subcat_id"],
                vote["alias_cat_type"],
            )

            if key not in grouped:
                grouped[key] = {
                    "category": vote["alias_cat_name"],
                    "subcategory": vote["alias_subcat_name"],
                    "category_type": vote["alias_cat_type"],
                    "ranking": [],
                }

            grouped[key]["ranking"].append(
                {
                    "id": vote["id"],
                    "name": vote["name"],
                    "cover": vote.get("cover"),
                    "profile_image": vote.get("profile_image"),
                    "grade": vote.get("grade"),
                    "group": vote.get("group"),
                    "course": vote.get("course"),
                    "total_votes": vote["alias_total_votes"],
                }
            )

        results.extend(grouped.values())

    return results
