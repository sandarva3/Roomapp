from django.contrib import admin
from .models import Room, Files

class RoomAdmin(admin.ModelAdmin):
    list_display = ['code']

admin.site.register(Room, RoomAdmin)
