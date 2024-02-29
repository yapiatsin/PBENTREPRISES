from django.urls import path
from userauths import views
from .views import EditProfilView
from django.contrib.auth import views as auth_views
from .views import PasswordChangeView, CreateUserProfile

name = "userauths"

urlpatterns = [
    
    path("sign_up", views.registrerView, name="register"),
    path("sign_in", views.loginview, name="login"),
    path("decon", views.logout_view, name="log_out"),
    path("interne", views.interneView, name="intern"),
    path("profil", views.profile, name="profil_user"),
    path('createprofile', CreateUserProfile.as_view(), name="creat_profil"),
    path('edit_profile',EditProfilView.as_view(), name="edit_profil"),
    path('passwordchange/',PasswordChangeView.as_view(template_name="userauths/chang_password.html"), name="chang_pass"),
    path('password_success/',views.password_success, name="password_success"),
]
