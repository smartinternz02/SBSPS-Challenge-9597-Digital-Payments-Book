"""book URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from app import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home,name='home'),
    path('adminregister/', views.adminregister,name='adminregister'),
    path('customerregister/', views.customerregister,name='customerregister'),
    path('view/', views.adminview,name='view'),
    path('cview/', views.customer_view,name='cview'),
    path('view/<str:cid>', views.customer_details,name='customerdetails'),
    path('viewdebtcustomer/<str:cid>',views.customer_debt_details,name='viewdebtcustomer'),
    path('viewpaidcustomer/<str:cid>',views.customer_paid_details,name='viewpaidcustomer'), 
    path('login/', views.loginuser,name='login'),
    path('purchase/',views.purchase,name='purchase'),
    path('customerindex/',views.customerindex,name='customerindex'),
    path('adminindex/',views.adminindex,name='adminindex'),
    path('logout/', views.custom_logout,name='logout'),
    path('addcustomer/',views.addshop,name='addshop'),
    path('viewdept/',views.viewdept,name='viewdept'),
    path('viewpaid/',views.viewpaid,name='viewpaid'),

]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)