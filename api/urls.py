from django.urls import path
from api import views

urlpatterns = [
    #------------------------------------------------Admin-----------------------------------------------
    path('activity-autocomplete/', views.admin_view.ActivityAutocomplete.as_view(), name='activity-autocomplete'),
    path('category-autocomplete/', views.admin_view.CategoryAutocomplete.as_view(), name='category-autocomplete'),
    path('project-autocomplete/', views.admin_view.ProjectAutocomplete.as_view(), name='project-autocomplete'),
    path('subcategory-autocomplete/', views.admin_view.SubCategoryAutocomplete.as_view(), name='subcategory-autocomplete'),
    path('api/admin/create-activity', views.admin_view.create_activity, name='create_activity'),
    path('api/admin/update-activity/<int:activity_id>', views.admin_view.update_activity, name='update_activity'),
    path('api/admin/close-activity/<int:activity_id>', views.admin_view.close_activity, name='close_category'),
    path('api/admin/delete-activity/<int:activity_id>', views.admin_view.delete_activity, name='delete_activity'),
    path('api/admin/create-category', views.admin_view.create_category, name='create_category'),
    path('api/admin/delete-category/<int:category_id>', views.admin_view.delete_category, name='delete_category'),
    path('api/admin/create-subcategory', views.admin_view.create_subcategory, name='create_subcategory'),
    path('api/admin/delete-subcategory/<int:subcategory_id>', views.admin_view.delete_subcategory, name='delete_subcategory'),
    path('api/admin/create-project', views.admin_view.create_project, name='create_project'),
    path('api/admin/update-project/<int:project_id>', views.admin_view.update_project, name='update_project'),
    path('api/admin/delete-project/<int:project_id>', views.admin_view.delete_project, name='delete-project'),
    path('api/admin/create-stand', views.admin_view.create_subcategory, name='create_stand'),
    path('api/admin/delete-stand/<int:stand_id>', views.admin_view.delete_stand, name='delete_stand'),
    path('api/admin/create-member', views.admin_view.create_member, name='create_member'),
    #----------------------------------------Authentication----------------------------------------------
    path('api/register-voter', views.authentication_view.register_voter, name='register_voter'),
    path('api/login', views.authentication_view.voter_login, name='voter_login'),
    path('api/refresh', views.authentication_view.voter_refresh_token, name='refresh_token'),
    path('api/verify-email', views.authentication_view.verify_email, name='verify_email'),
    #--------------------------------------Get Views-----------------------------------------------------
    path('api/get-members', views.get_view.get_members, name='get_members'),
    path('api/count-voters', views.get_view.count_voters, name='count_voters'),
    path('api/get-member/<int:id>', views.get_view.get_member, name='get_member'),
    path('api/get-category-items', views.get_view.get_category_items, name='get_category'),
    path('api/get-projects', views.get_view.get_projects, name='get_projects'),
    path('api/get-project/<int:project_id>', views.get_view.get_project, name='get_project'),
    path('api/count-project', views.get_view.count_project, name='count_project'),
    path('api/count-activity', views.get_view.count_activity, name='count_activty'),
    path('api/count-members', views.get_view.count_members, name='count_members'),
    path('api/get-votes', views.get_view.get_votes, name='get_votes'),
    path('api/get-activities', views.get_view.get_activities, name='get_activities'),
    path('api/get-activity/<int:activity_id>', views.get_view.get_activity, name='get_activity'),
    path('api/count-project-by-category/<int:activity_id>', views.get_view.count_project_in_category, name='count_project_by_category'),
    path('api/get-members-by-category/<int:category_id>', views.get_view.get_members_by_category, name='get_members_by_category'),
    path('api/get-categories/<int:activity_id>', views.get_view.get_categories_by_activity, name='get_categories'),
    path('api/get-category/<int:category_id>', views.get_view.get_category, name='get_category'),
    path('api/get-subcategories', views.get_view.get_subcategories, name='get_subcategories'),
    path('api/get-subcategory/<int:id>', views.get_view.get_subcategory, name='get_subcategory'),
    path('api/get-top-projects', views.get_view.top_projects, name='top_projects'),
    path('api/count-project-in-activity/<int:activity_id>', views.get_view.activity_project_count, name='count_project_activity'),
    path('api/get-me', views.get_view.get_me, name='get_voter'),
    #------------------------------------ Ranking View---------------------------------------------------
    path('api/get-voters/', views.ranking_view.VoterListView.as_view(), name='get_voters'),
    path('api/get-rankings/<int:activity_id>', views.ranking_view.RankingView.as_view(), name='get_ranking_category'),
    path('api/subcategoryProjectsRanking/<int:subcategory_id>/', views.ranking_view.SubcategoryProjectRankingView.as_view(), name='subcategory-project-ranking'),
    path('api/public-rankings/<int:activity_id>', views.ranking_view.PublicRankingView.as_view(), name='public_ranking_category'),
    path('api/verify-activity/<int:activity_id>', views.ranking_view.VerifyActivity.as_view(), name='verify_activity'),
    #-------------------------------Vote View--------------------------------------------------------------
    path('api/vote', views.vote_view.vote, name='vote')
]
