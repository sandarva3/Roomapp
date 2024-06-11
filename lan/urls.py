from django.urls import path
from .views import(
    lan_view,
    async_view,
)

urlpatterns = [
    path('', lan_view, name='lan'),
    path('async/', async_view, name='async'),
]
