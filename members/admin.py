from django.contrib import admin
from core.models import Member  # import the centralised model


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    """
    Admin configuration for Member.
    Kept in the 'members' app to keep UI/admin concerns near the feature,
    while the data model stays centralised in 'core'.
    """
    list_display = ("name", "email", "status", "created_at", "updated_at")
    list_filter = ("status", "created_at")
    search_fields = ("name", "email")
    ordering = ("name",)
    date_hierarchy = "created_at"

    readonly_fields = ("created_at", "updated_at")
    fields = ("name", "email", "status", "created_at", "updated_at")

    actions = ["mark_current", "mark_ex_member", "toggle_selected"]

    def mark_current(self, request, queryset):
        """Bulk-mark selected members as CURRENT."""
        updated = queryset.update(status=Member.Status.CURRENT)
        self.message_user(request, f"{updated} member(s) marked as Current.")
    mark_current.short_description = "Mark selected as Current"

    def mark_ex_member(self, request, queryset):
        """Bulk-mark selected members as EX_MEMBER."""
        updated = queryset.update(status=Member.Status.EX_MEMBER)
        self.message_user(request, f"{updated} member(s) marked as Ex-Member.")
    mark_ex_member.short_description = "Mark selected as Ex-Member"

    def toggle_selected(self, request, queryset):
        """
        Bulk-toggle status for selected members using model logic.
        """
        toggled = 0
        for obj in queryset:
            obj.toggle_status(save=True)
            toggled += 1
        self.message_user(request, f"Toggled status for {toggled} member(s).")
    toggle_selected.short_description = "Toggle status for selected"
