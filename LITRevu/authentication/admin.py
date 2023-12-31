from django.contrib import admin

from authentication.models import User
    
class UserAdmin(admin.ModelAdmin):
    list_display = ('role', 'follows')
    
admin.site.register(User)