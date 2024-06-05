from django.urls import path,include
from . import views
# from .views import EmployeeList=
from django.urls import path

urlpatterns = [
    path('token_verify/', views.verify_token , name='token'),
    path('register_api/', views.employee_list, name='register_api'),
    path('register/', views.registration, name='registration'),
    path('login/', views.login, name='login'),
    path('login_api/', views.login_api, name='login_api'),
    path('home/', views.index, name='index'),
    path('profile/',views.Profile,name="profile"),
    path('profile_api/',views.Profile,name="profile_api"),

    
]