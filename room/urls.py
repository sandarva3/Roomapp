from django.urls import path
from uuid import UUID

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
