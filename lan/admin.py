from django.contrib import admin
from .models import Text, Lanfiles, FilesHistory

admin.site.register(Text)
admin.site.register(Lanfiles)

@admin.register(FilesHistory)
class FilesHistory(admin.ModelAdmin):
    list_display = ('file_name', 'Triggered_at', 'Faddress')
    readonly_fields = ('Triggered_at',)
    list_filter = ('Triggered_at',)
    search_fields = ('file_name',)