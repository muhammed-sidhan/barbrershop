from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.sitemaps.views import sitemap
from django.contrib.sitemaps import Sitemap
from django.urls import reverse

class StaticSitemap(Sitemap):
    def items(self):
        return [
            
            'index',
            'role_based_home',
            'barber_register',
            'customer_register',
            'login',
            'customer_barber_list',
        ]

    def location(self, item):
        return reverse(item)

# ✅ Create instance of sitemap class
sitemaps = {
    'static': StaticSitemap(),
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),

    # Sitemap and robots.txt
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='sitemap'),
    path('robots.txt', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),

    # Google site verification
    path('google1234567890abcdef.html',
         TemplateView.as_view(template_name='google1234567890abcdef.html', content_type='text/html')),
]
