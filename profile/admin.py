from django.contrib import admin
from .models import ServersBuffer
from servers.models import Servers, Tags, Colors, Banners, Illustrations


class ServersAdmin(admin.ModelAdmin):
    search_fields = ['name']


admin.site.register(ServersBuffer)
admin.site.register(Servers, ServersAdmin)
admin.site.register(Colors)
admin.site.register(Tags)
admin.site.register(Banners)
admin.site.register(Illustrations)
