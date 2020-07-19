from django.contrib import admin
from .models import Purchase, MultiPlayerInvite
# Register your models here.


class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'completed_status', 'playing_status')


admin.site.register(Purchase, PurchaseAdmin)


class MultiPlayerInviteAdmin(admin.ModelAdmin):
    list_display = ('__str__', )


admin.site.register(MultiPlayerInvite, MultiPlayerInviteAdmin)
