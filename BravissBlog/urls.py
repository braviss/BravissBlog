from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from blog.views import HomePageView
from django.contrib.sitemaps.views import sitemap
from blog.sitemaps import ArticleSitemap
from django.views.generic.base import TemplateView

sitemaps = {
    'articles' : ArticleSitemap,
}

urlpatterns = [
    path("sitemap.xml",
         sitemap,
         {"sitemaps": sitemaps},
         name="django.contrib.sitemaps.views.sitemap"),
    path("robots.txt",
         TemplateView.as_view(template_name="robots.txt",
                              content_type="text/plain")
         ),
    path('admin/doc/',
         include('django.contrib.admindocs.urls')),
    path('admin/',
         admin.site.urls),
    path('tinymce/',
         include('tinymce.urls')),
]

urlpatterns += i18n_patterns(
    path('',
         HomePageView.as_view(), name='home'),
    path('accounts/',
         include(('accounts.urls', 'accounts'), namespace='accounts')),
    path('blog/',
         include(('blog.urls', 'blog'), namespace='blog')),
    path('i18n/',
         include('django.conf.urls.i18n')),
) + static(settings.MEDIA_URL,
           document_root=settings.MEDIA_ROOT)
