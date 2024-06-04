from django.urls import path
from .views import(
    lan_view,
)

urlpatterns = [
    path('', lan_view, name='lan'),
]
