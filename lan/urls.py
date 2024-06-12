from django.urls import path
from .views import(
    lan_view,
    async_view,
    files_view,
)

urlpatterns = [
    path('', lan_view, name='lan'),
    path('async/', async_view, name='async'),
    path('files/', files_view, name='lanfiles'),
]
