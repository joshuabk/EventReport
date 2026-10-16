from django.contrib import admin
from .models import ActivityLog


@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ("timestamp", "username", "action", "report_id", "details", "ip_address")
    list_filter = ("action", "username")
    search_fields = ("username", "details", "report_id")
    readonly_fields = ("timestamp", "user", "username", "action", "report_id", "details", "ip_address")

    # The log is append-only: nobody edits or deletes rows from the admin.
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
