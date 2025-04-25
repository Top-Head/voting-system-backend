from django.urls import path
from api import views
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
# ---------------------------------------------Admin-----------------------------------------------
    path('api/token/', views.AdminLogin.as_view(), name='Obtain-Token'),



#---------------------------------------------Voter-------------------------------------------------
]