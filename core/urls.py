
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
handler404 = 'KENETAssets.views.custom_404'
handler500 = 'KENETAssets.views.custom_505'
from KENETAssets.views import *

# admin.site.site_header = '.'                    # default: "Django Administration"
admin.site.index_title = 'Assets Management Area '                 # default: "Site administration"
admin.site.site_title = 'KENET admin panel' # default: "Django site admin"


urlpatterns = [
    path('admin/', admin.site.urls),
    path('app/', include('KENETAssets.urls')),
    path('', home_view, name='home'),
    path('api/', include('version_control.urls')),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)