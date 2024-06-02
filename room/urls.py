from django.urls import path
from uuid import UUID
from django.conf import settings
from django.conf.urls.static import static

from.views import(
    home_view,
    room_view,
    link_view,
    ajax_view,
)

urlpatterns = [
    path('', home_view, name='home'),
    path('room/', room_view, name='room'),
    path('room/<uuid:uuid>', link_view, name="roomlink"),
    path('endpoint', ajax_view, name='sendajax'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)