from django.contrib import admin
from .models import EmailSender

class EmailSenderAdmin(admin.ModelAdmin):
    list_display = (
        'sent_on',
        'opened',
        'is_first_email',
        'destination',
    )
    exclude = (
        'base_token',
        'sent_on',
        'opened',
    )

admin.site.register(EmailSender, EmailSenderAdmin)
