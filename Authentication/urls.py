from django.urls import path,include
from . import views
# from .views import EmployeeList=
from django.urls import path
from .views import ProductCreateAPIView,ProductUpdateDeleteView

urlpatterns = [
    path('token_verify/', views.verify_token , name='token'),
    path('register_api/', views.employee_list, name='register_api'),
    path('register/', views.registration, name='registration'),
    path('login/', views.login, name='login'),
    path('login_api/', views.login_api, name='login_api'),
    path('home/', views.index, name='index'),
    path('profile/',views.Profile,name="profile"),
    # path('profile_api/',views.profile_api,name="profile_api"),
    path('get_profile_details/',views.get_profile_details,name="get_profile_details"),
    path('Edit_profile_details/',views.Edit_profile_details,name="Edit_profile_details"),  
    path('update_profile/',views.Edit_profile_details,name="update_profile"),
    path('About_us/',views.about,name="About_us"),
    path('contact_us/',views.contact_us,name="contact_us"),
    path('product/',views.add_product,name="product"),
    path('view_all_product/',views.view_all_product,name='view_all_product'),
    path('Product_description/<slug:slug>',views.Product_description,name='Product_description'),
    path('add_product_api/', ProductCreateAPIView.as_view()),
    path('update_delete_product/<slug:slug>', ProductUpdateDeleteView.as_view()),  
    path('accounts/', include('allauth.urls')),
]