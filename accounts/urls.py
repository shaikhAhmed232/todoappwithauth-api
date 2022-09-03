from django.urls import path

from . import views

urlpatterns = [
    path('signup/', views.SignUp.as_view(), name="signup"),
    path('login/', views.Login.as_view(), name="login"),
    # path("get-csrf/",views.get_csrf, name="get_csrf"),
    path("logout/", views.LogoutView.as_view(), name="logout_view"),
    path('current/', views.GetCurrentUser.as_view(), name="current_user"),
]
