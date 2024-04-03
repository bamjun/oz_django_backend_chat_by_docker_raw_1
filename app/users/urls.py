from django.urls import path
from . import views

urlpatterns = [
		path("login", views.Login.as_view(), name='login') ,  # django session login
    path("logout", views.Logout.as_view(), name='logout'), # django session logout
    path("register", views.Signup.as_view(), name='register'), # django
    path("", views.login_page),
    path("signup", views.signup_page)
]
