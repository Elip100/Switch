from django.urls import path
from . import views

urlpatterns = [
    path("", views.indexView, name="index"),
    path("login/", views.choose_account_option),
    path("verifylogin/", views.VerifyLogin),
    path("logout/", views.Logout),
    path("project/<int:project_id>/", views.projectView)
]