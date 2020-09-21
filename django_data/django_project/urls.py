from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Django admin
    path('admin/', admin.site.urls),

    # Local apps
    path('', include('persons.urls')),
    path('tree/', include('tree.urls')),
]

if bool(settings.DEBUG):
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
