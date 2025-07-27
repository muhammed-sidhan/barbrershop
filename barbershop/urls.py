"""
URL configuration for barbershop project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.views.generic import TemplateView
from django.contrib.sitemaps.views import sitemap
from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('core.urls')),
     # robots.txt served from template
    path('robots.txt', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),
]

class StaticSitemap(Sitemap):
    def items(self):
        return ['home', 'index',
            'role_based_home',
            'barber_register',
            'customer_register',
            'login',
            'customer_barber_list', # lists all barbers
            ]    # Add more named URLs as needed

    def location(self, item):
        return reverse(item)

sitemaps = {
    'static': StaticSitemap,
}

urlpatterns += [
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('google1234567890abcdef.html',
         TemplateView.as_view(template_name='google1234567890abcdef.html',
                              content_type='text/html')),
]
