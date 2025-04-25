from django.urls import path
from api import views

urlpatterns = [
# ---------------------------------------------Admin-----------------------------------------------
    path('api/admin_login/', views.admin_login, name='admin_token'),



#---------------------------------------------Voter-------------------------------------------------
]