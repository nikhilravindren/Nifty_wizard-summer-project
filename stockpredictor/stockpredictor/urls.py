"""
URL configuration for stockpredictor project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from stockuser import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home,name='home'),
    path('login',views.user_user_login,name='login'),
    path('logout',views.user_logout,name='logout'),
    path('create-account',views.create_ac,name='create'),
    path('about/',views.about,name='about'),
    path('services/',views.services,name='service'),
    path('why-us/',views.why,name='why'),
    path('stocks/',views.stock,name='stocks'),
    path('stock_details/<str:symbol>',views.stock_detail,name='stock_details'),
    path('search/', views.search_stock, name='search_stock'),
    path('prediction_day/<str:symbol>',views.predicting_1,name='predicting_1'),
    # path('prediction_week/<str:symbol>',views.predicting_7,name='predicting_7'),
    # path('prediction1_month/<str:symbol>',views.predicting_30,name='predicting_30'),
    path('concern/',views.concern,name='concern'),
]
