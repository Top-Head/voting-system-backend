from django.urls import path
from api import views

urlpatterns = [
    #------------------------------------------------Admin-----------------------------------------------
    path('activity-autocomplete/', views.admin_view.ActivityAutocomplete.as_view(), name='activity-autocomplete'),
    path('subcategory-autocomplete/', views.admin_view.SubCategoryAutocomplete.as_view(), name='subcategory-autocomplete'),
    path('api/create-activity', views.admin_view.create_activity, name='create_activity'),
    path('api/admin/close-activity/<int:id>', views.admin_view.close_activity, name='close_category'),
    path('api/admin/create-project', views.admin_view.create_project, name='create_project'),
    path('api/admin/update-project/<int:id>', views.admin_view.update_project, name='update_project'),
    #----------------------------------------Authentication----------------------------------------------
    path('api/register-voter', views.authentication_view.register_voter, name='register_voter'),
    path('api/login', views.authentication_view.voter_login, name='voter_login'),
    path('api/verify-email', views.authentication_view.verify_email, name='verify-email'),
    #--------------------------------------Get Views-----------------------------------------------------
    path('api/get-members', views.get_view.get_members, name='get_members'),
    path('api/get-member/<int:id>', views.get_view.get_member, name='get_member'),
    path('api/get-category-items', views.get_view.get_category_items, name='get_category'),
    path('api/get-projects', views.get_view.get_projects, name='get_projects'),
    path('api/get-project/<int:id>', views.get_view.get_project, name='get_project'),
    path('api/count-project', views.get_view.count_project, name='count_project'),
    path('api/count-category', views.get_view.count_category, name='count_category'),
    path('api/get-votes', views.get_view.get_votes, name='get_votes'),
    path('api/get-activities', views.get_view.get_activities, name='get_activities'),
    path('api/get-activity/<int:id>', views.get_view.get_activity, name='get_activity'),
    path('api/count-project-by-category', views.get_view.count_project_in_category, name='count_project_by_category'),
    path('api/get-members-by-category/<int:category_id>', views.get_view.get_members_by_category, name='get_members_by_category'),
    path('api/get-subcategories', views.get_view.get_subcategories, name='get_subcategories'),
    path('api/get-subcategory/<int:id>', views.get_view.get_subcategory, name='get_subcategory'),
    path('api/get-me', views.get_view.get_me, name='get_voter'),
    #------------------------------------ Ranking View---------------------------------------------------
    path('api/get-voters/', views.ranking_view.VoterListView.as_view(), name='get_voters'),
    path('api/get-rankings/<int:activity_id>', views.ranking_view.RankingView.as_view(), name='get_ranking_category'),
    path('api/subcategoryProjectsRanking/<int:subcategory_id>/', views.ranking_view.SubcategoryProjectRankingView.as_view(), name='subcategory-project-ranking'),
    path('api/public-rankings/<int:activity_id>', views.ranking_view.PublicRankingView.as_view(), name='public_ranking_category'),
    path('api/get-categories', views.get_view.get_categorys, name='get_categories'),
    path('api/verify-activity/<int:activity_id>', views.ranking_view.VerifyActivity.as_view(), name='verify_activity'),
    #-------------------------------Vote View--------------------------------------------------------------
    path('api/vote', views.vote_view.vote, name='vote_project')
]
