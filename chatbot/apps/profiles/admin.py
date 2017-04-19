from django.contrib import admin

from . import models


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'profile_url_as_a',)

    def profile_url_as_a(self, obj):
        return '<a href="%s">%s</a>' % (obj.profile_url, obj.profile_url)

    profile_url_as_a.allow_tags = True
    profile_url_as_a.short_description = 'Profile URL'


admin.site.register(models.UserProfile, UserProfileAdmin)
admin.site.register(models.ExpertNoteTemplate)
