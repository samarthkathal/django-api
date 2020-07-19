from django.contrib import admin
from .models import Game, Collection

# Register your models here.


class GameAdmin(admin.ModelAdmin):
	list_display = ('name', 'collection_name', 'collection_id')
 

admin.site.register(Game, GameAdmin)

#admin.site.register(Game)
admin.site.register(Collection)

