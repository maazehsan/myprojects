from django.contrib import admin
from .models import Message

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('user', 'subject', 'short_message')
    search_fields = ('user__username', 'subject', 'message')
    list_filter = ('user',)
    
    def short_message(self, obj):
        return (obj.message[:50] + '...') if obj.message and len(obj.message) > 50 else obj.message
    short_message.short_description = 'Message Preview'
