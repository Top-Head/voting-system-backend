from django.urls import path
from api import views

urlpatterns = [
    path('activity-autocomplete/', views.ActivityAutocomplete.as_view(), name='activity-autocomplete'),
    path('category-autocomplete/', views.CategoryAutocomplete.as_view(), name='category-autocomplete'),
    path('subcategory-autocomplete/', views.SubCategoryAutocomplete.as_view(), name='subcategory-autocomplete'),
    path('api/admin/close-activity/<int:id>', views.close_activity, name='close_category'),
    path('api/admin/create-project', views.create_project, name='create_project'),
    path('api/admin/update-project/<int:id>', views.update_project, name='update_project'),
    path('api/login', views.voter_login, name='voter_login'),
    path('api/get-members', views.get_members, name='get_members'),
    path('api/get-member/<int:id>', views.get_member, name='get_member'),
    path('api/get-category-items', views.get_category_items, name='get_category'),
    path('api/get-projects', views.get_projects, name='get_projects'),
    path('api/get-project/<int:id>', views.get_project, name='get_project'),
    path('api/count-project', views.count_project, name='count_project'),
    path('api/count-category', views.count_category, name='count_category'),
    path('api/vote', views.vote, name='vote_project'),
    path('api/get-votes', views.get_votes, name='get_votes'),
    path('api/create-activity', views.create_activity, name='create_activity'),
    path('api/get-activities', views.get_activities, name='get_activities'),
    path('api/get-activity/<int:id>', views.get_activity, name='get_activity'),
    path('api/count-projct-by-category', views.count_project_in_category, name='count_project_by_category'),
    path('api/register-voter', views.register_voter, name='register_voter'),
    path('api/get-members-by-category/<int:category_id>', views.get_members_by_category, name='get_members_by_category'),
    path('api/get-subcategories', views.get_subcategories, name='get_subcategories'),
    path('api/get-subcategory/<int:id>', views.get_subcategory, name='get_subcategory'),
    path('api/get-voters/', views.VoterListView.as_view(), name='get_voters'),
    path('api/get-rankings/<int:activity_id>', views.RankingView.as_view(), name='get_ranking_category'),
    path('api/get-me', views.get_me, name='get_voter'),
    path('api/subcategoryProjectsRanking/<int:subcategory_id>/', views.SubcategoryProjectRankingView.as_view(), name='subcategory-project-ranking'),
    path('api/public-rankings/<int:activity_id>', views.PublicRankingView.as_view(), name='public_ranking_category'),
    path('api/get-categories', views.get_categorys, name='get_categories'),
    path('api/verify-activity/<int:activity_id>', views.VerifyActivity.as_view(), name='verify_activity'),
]
