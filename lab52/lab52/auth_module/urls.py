from django.urls import path, re_path
from . import views

app_name = 'auth_module'

urlpatterns = [
    re_path(r'^registration/$', views.RegistrationView.as_view(), name='registration'),
    re_path(r'^login/$', views.SignInFormView.as_view(), name='login'),
    re_path(r'^logout/$', views.LogoutFormView.as_view(), name='logout'),
    re_path(r'^profile/$', views.ProfileView.as_view(), name='profile'),
    re_path(r'^edit_profile/$', views.EditProfileView.as_view(), name='edit_profile'),
]