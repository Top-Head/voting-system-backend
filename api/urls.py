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
]