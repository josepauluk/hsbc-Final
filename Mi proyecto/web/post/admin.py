from django.contrib import admin

from .models import Post

class PostAdmin(admin.ModelAdmin):
    list_display = ("foto",)
    search_fields = ("foto",)
    ordering = ("foto",)
    
admin.site.register(Post, PostAdmin)
