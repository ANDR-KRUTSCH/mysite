"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.contrib.sitemaps.views import sitemap

from blog.sitemaps import PostSitemap

sitemaps = dict(sitemaps=PostSitemap)

urlpatterns = (
    path(route='admin/', view=admin.site.urls),
    path(route='blog/', view=include(arg='blog.urls', namespace='blog')),
    path(route='sitemap.xml', view=sitemap, kwargs=dict(sitemaps=sitemaps), name='django.contrib.sitemaps.views.sitemap'),
)