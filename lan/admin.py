from django.contrib import admin
from .models import Text, Lanfiles, FilesHistory

admin.site.register(Text)
admin.site.register(Lanfiles)
admin.site.register(FilesHistory)