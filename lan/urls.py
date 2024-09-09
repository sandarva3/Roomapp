from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .views import(
    lan_view,
    async_view,
    files_view,
    delFile_view,
    lanAjax_view,
    first_view,
    about_view,
    removeAllFiles_view,
    faq_view,
    largeFiles_view,
)

urlpatterns = [
    path('', first_view, name='first'),
    path('lan/', lan_view, name='lan'),
    path('async/', async_view, name='async'),
    path('files/', files_view, name='lanfiles'),
    path('del/<int:id>', delFile_view, name='delfile'),
    path('lanEndpoint', lanAjax_view, name='lanAjax'),
    path('about/', about_view, name='about'),
    path('removeAll/', removeAllFiles_view, name='removeAll'),
    path('faq/', faq_view, name='faq'),
    path('largeFiles/', largeFiles_view, name='largeFiles'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
