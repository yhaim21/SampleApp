"""SampleApp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path, include
from sample_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('',views.entry,name="entry"),
    path('home',views.home,name="home"),
    path('html_tests/divs', views.show3divs, name="showdivs"),
    path('form',views.showform,name='showform'),
    path('django/tango/formresults', views.form_results, name="showformresults"),
    path('maintenance', views.maintenance, name='maintenance'),
    path('currency-selection',views.currency_selection,name="currency_selector"),
    path('company_info',views.company_selection,name="company_info"),
    path('register',views.register_new_user,name="register_user"),

]
