from django.contrib import admin
from .models import Friendship# ,Request 

# Register your models here.

#admin.site.register(Request)
#admin.site.register(Friendship)


#class FriendshipRequestAdmin(admin.ModelAdmin):
#    date_hierarchy = 'created'
#    list_display = ('from_user', 'to_user', 'created')
#    actions = ('accept_friendship', 'decline_friendship', 'cancel_friendship')
#
#    def accept_friendship(self, request, queryset):
#        for request in queryset:
#            request.accept()
#
#    def decline_friendship(self, request, queryset):
#        for request in queryset:
#            request.decline()
#    
#    def cancel_friendship(self, request, queryset):
#        for request in queryset:
#            request.cancel()
# 
#
#admin.site.register(Request, FriendshipRequestAdmin)


class FriendshipAdmin(admin.ModelAdmin):
    list_display = ('user', 'friend_count')


admin.site.register(Friendship, FriendshipAdmin)

