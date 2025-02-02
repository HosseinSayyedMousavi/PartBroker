from django.urls import path , include
from . import views
from rest_framework_simplejwt.views import TokenRefreshView,TokenVerifyView,TokenObtainPairView
app_name = "accounts"

urlpatterns = [
    # register 
    path("register/",views.RegistrationApiView.as_view(),name = 'register'),
    # login jwt
    path("login/",TokenObtainPairView.as_view() , name = "login"),
    path("refresh/",TokenRefreshView.as_view() , name = "jwt-refresh"),
    path("verify/",TokenVerifyView.as_view() , name = "jwt-verify"),
    # user update
    path("user_info/",views.UserAPIView.as_view() , name = "user-info")
    ]