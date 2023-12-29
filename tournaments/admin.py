from django.contrib import admin
from tournaments.models import Bedwars


class BedwarsAdmin(admin.ModelAdmin):
    list_display = ['team', 'working_status', 'completed_status', 'approved_status']


admin.site.register(Bedwars, BedwarsAdmin)
