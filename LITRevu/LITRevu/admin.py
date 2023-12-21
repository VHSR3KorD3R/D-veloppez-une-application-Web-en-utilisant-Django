from django.contrib import admin

from LITRevu.models import Ticket, Review

class TicketAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'user', 'image', 'time_created')
    
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('ticket','rating', 'headline', 'body', 'user', 'time_created')
    
admin.site.register(Ticket)
admin.site.register(Review)
