
from django.urls import path

from user import views


urlpatterns = [

    path('login', views.login),
    path('register',views.register),
    path('index', views.index),
    path('test',views.test),
    path('about',views.about),

    path('queryre', views.queryre),
    path('search', views.search),
    path('loginout',views.logingout),
    path('download' , views.download),
    path('check_login',views.check_login),
    #
    path('queryre_1',views.queryre_1),
    path("get_allheaders",views.get_allheaders),
    path('Home' , views.Home),
    path('Login_page' , views.Login_page),
    path('Introduction' , views.Introduction),
    path('About_us' , views.About_us),
    path('Access_data' , views.Access_data),
    path('by_interstatioal_water' , views.by_interstatioal_water),
    path('by_cnhs' , views.by_cnhs),
    path('by_sra', views.by_sra),
    path('by_element', views.by_element),
    path('by_age', views.by_age),
    path('by_location', views.by_location),
    path('by_program', views.by_program),
    path('general_search', views.general_search),
    path('search_download', views.search_download),
    path('search_result', views.search_result),
    path('check_user', views.check_user),

]
