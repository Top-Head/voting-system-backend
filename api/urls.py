from django.urls import path
from api import views

urlpatterns = [
# ---------------------------------------------Admin-----------------------------------------------
    path('category-autocomplete/', views.CategoryAutocomplete.as_view(), name='category-autocomplete'),
    path('api/admin/create-category', views.create_category, name='create_category'),
    path('api/admin/update-category/<int:id>', views.update_category, name='update_category'),
    path('api/admin/close-activity/<int:id>', views.close_activity, name='close_category'),
    path('api/admin/create-project', views.create_project, name='create_project'),
    path('api/admin/update-project/<int:id>', views.update_project, name='update_project'),
#---------------------------------------------Voter-------------------------------------------------
    path('api/login', views.voter_login, name='voter_login'),
    path('api/vote-project', views.vote_project, name='vote_poject'),
    path('api/vote-expositor', views.vote_expositor, name='vote_expositor'),
    path('api/get-members', views.get_members, name='get_members'),
    path('api/get-categorys', views.get_categorys, name='get_categorys'),
    path('api/get-category/<int:id>', views.get_category, name='get_category'),
    path('api/get-projects', views.get_projects, name='get_projects'),
    path('api/get-project/<int:id>', views.get_project, name='get_project'),
    path('api/count-project', views.count_project, name='count_project'),
    path('api/count-category', views.count_category, name='count_category'),
    path('api/vote-project', views.vote_project, name='vote_project'),
    path('api/vote-expositor', views.vote_expositor, name='vote_expositor'),
    path('api/ranking/projects/<int:category_id>/', views.ProjectRankingView.as_view(), name='project-ranking'),
    path('api/ranking/members/<int:category_id>/', views.MemberRankingView.as_view(), name='member-ranking'),
    path('api/get-votes', views.get_votes, name='get_votes'),
    path('api/create-activity', views.create_activity, name='create_activity'),
    path('api/get-activities', views.get_activities, name='get_activities'),
    path('api/get-activity/<int:id>', views.get_activity, name='get_activity'),
    path('api/update-activity/<int:id>', views.update_activity, name='update_activity'),
    path('api/cretae-member', views.create_member, name='create_member'),
    path('api/count-projct-by-category', views.count_project_in_category, name='count_project_by_category'),
    path('api/register-voter', views.register_voter, name='register_voter')
]