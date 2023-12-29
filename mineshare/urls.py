from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from sitemap.views import robots
from django.conf.urls.static import static


admin.site.site_header = "Mineshare - Панель управления"
admin.site.site_title = "Mineshare - Панель управления"
admin.site.index_title = "Mineshare - Панель управления"


urlpatterns = [
    path('', include('allauth.urls')),
    path('admin/', admin.site.urls),
    path('account/', include('profile.urls')),
    path('', include('servers.urls')),
    path('shop/', include('shop.urls')),
    path('news/', include('news.urls')),
    path('tournaments/', include('tournaments.urls')),
    path('home/', include('home.urls')),
    path('support/', include('support.urls')),
    path('sitemap.xml', include('sitemap.urls')),
    path('sitemap/', include('sitemap.urls')),
    path('robots.txt', robots),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'home.views.error404'
handler500 = 'home.views.error500'