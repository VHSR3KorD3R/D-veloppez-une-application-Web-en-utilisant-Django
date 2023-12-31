from django.contrib import admin

from LITRevu.models import Ticket, Review, UserFollows

class TicketAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'user', 'image', 'time_created')
    
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('ticket','rating', 'headline', 'body', 'user', 'time_created')

class UserFollowsAdmin(admin.ModelAdmin):
    list_display = ('user','followed_user')

admin.site.register(Ticket)
admin.site.register(Review)
admin.site.register(UserFollows)
# admin.site.register(follows)