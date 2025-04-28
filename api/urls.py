from django.urls import path
from api import views

urlpatterns = [
# ---------------------------------------------Admin-----------------------------------------------
    path('api/admin/login', views.admin_login, name='admin_token'),
    path('api/admin/create-category', views.create_category, name='create_category'),
    path('api/admin/update-category/<int:id>', views.update_category, name='update_category'),
    path('api/admin/close-category/<int:id>', views.close_category, name='close_category'),
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
]