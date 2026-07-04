from django.contrib import admin
from django.urls import path, include

from dashboard.views import home
from recommendations.views import recommendation_dashboard

urlpatterns = [

    path(
        'admin/',
        admin.site.urls
    ),

    path(
        '',
        home,
        name='home'
    ),

    path(
        'accounts/',
        include('accounts.urls')
    ),

    path(
        'resources/',
        include('resources_app.urls')
    ),

    path(
        'test123/',
        home,
        name='test123'
    ),

    path(
        'recommendations/',
        recommendation_dashboard,
        name='recommendations'
    ),

]