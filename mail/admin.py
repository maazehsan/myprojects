from django.contrib import admin
from .models import Email

@admin.register(Email)
class EmailAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'sender', 'subject', 'timestamp', 'read', 'archived')
    list_filter = ('read', 'archived', 'timestamp')
    search_fields = ('subject', 'body', 'sender__username', 'recipients__username')
    filter_horizontal = ('recipients',)
    ordering = ('-timestamp',)
