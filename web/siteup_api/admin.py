from django.contrib import admin

from siteup_api.models import *


# Register your models here.

class UserExtraAdmin(admin.ModelAdmin):
    pass
admin.site.register(UserExtra, UserExtraAdmin)


class CheckLogAdmin(admin.ModelAdmin):
    list_display = ('status', 'get_check_type', 'get_check_target', 'get_check_owner')
    search_fields = ['check__group__owner']

    def get_check_type(self, obj):
        return obj.check.__class__.__name__

    get_check_type.short_description = 'Check type'

    def get_check_target(self, obj):
        return obj.check.target
    get_check_target.short_description = 'Check target'

    def get_check_owner(self, obj):
        return obj.check.group.owner.username
    get_check_owner.short_description = 'Check owner'

admin.site.register(CheckLog, CheckLogAdmin)


class CheckStatusAdmin(admin.ModelAdmin):
    list_display = ('get_check_title', 'status', 'date_start')

    def get_check_title(self, obj):
        return obj.check.__class__.__name__ + " - " + obj.check.title
    get_check_title.short_description = 'Check title'

admin.site.register(CheckStatus, CheckStatusAdmin)


class PingCheckAdmin(admin.ModelAdmin):
    list_display = ('target', 'timeout_value', 'get_owner')

    def get_owner(self, obj):
        return obj.group.owner.username
    get_owner.short_description = 'Owner'


admin.site.register(PingCheck, PingCheckAdmin)


class PortCheckAdmin(admin.ModelAdmin):
    list_display = ('target', 'target_port', 'response_check_string', 'get_owner')

    def get_owner(self, obj):
        return obj.group.owner.username
    get_owner.short_description = 'Owner'

admin.site.register(PortCheck, PortCheckAdmin)


class HttpCheckAdmin(admin.ModelAdmin):
    list_display = ('target', 'status_code', 'content_check_string', 'get_owner')

    def get_owner(self, obj):
        return obj.group.owner.username
    get_owner.short_description = 'Owner'

admin.site.register(HttpCheck, HttpCheckAdmin)


class DnsCheckAdmin(admin.ModelAdmin):
    list_display = ('target', 'record_type', 'resolved_address', 'get_owner')

    def get_owner(self, obj):
        return obj.group.owner.username
    get_owner.short_description = 'Owner'

admin.site.register(DnsCheck, DnsCheckAdmin)


class CheckGroupAdmin(admin.ModelAdmin):
    pass
admin.site.register(CheckGroup, CheckGroupAdmin)
