"""ounceServer2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path,include
from .views import login1,registration,sendUserVerficationOtp
from .connectionView import formsGet
from .mainView import HelloView,UserDetails,AddAddress,DisplayAllAddress\
    ,DeleteAddress,DisplayAllOrders,rateApi,AddNewCompany,EditMyCompany,DisplayMyCompany
from .TransactionViews import BuyCommodity,SellCommodity,ExchangeCommodity
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path("",formsGet),
    path("api/",HelloView.as_view(),name="hallowView"),
    path('login/' ,obtain_auth_token, name='api_token_auth'),
    path("registration/",registration),
    path("sendOtp/",sendUserVerficationOtp),
    path("displayUser/",UserDetails.as_view()),
    path("addAddress/",AddAddress.as_view()),
    path("deleteAddress/",DeleteAddress.as_view()),
    path("displayAllAddress/",DisplayAllAddress.as_view()),
    path("buy/",BuyCommodity.as_view()),
    path("sell/",SellCommodity.as_view()),
    path("displayAllOrders/",DisplayAllOrders.as_view()),
    path("rateApi/",rateApi),
    path("addCompany/",AddNewCompany),
    path("editCompany/",EditMyCompany),
    path("displayCompany/",DisplayMyCompany),
    path("Exchange/",ExchangeCommodity)



]
