from django.db import models
from datetime import date
import uuid


class GameManager(models.Manager):
	def collection_id(self, gamename):
		return Game.objects.get(name=gamename).collection.id


# Create your models here.
class Collection(models.Model):
    collectionname = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.collectionname

class Game(models.Model):
	gameid = models.AutoField(primary_key=True)
	groupid = models.CharField(default=uuid.uuid4, editable=True, max_length=40)
	name = models.CharField(max_length=50, null=False, unique=True, blank=False)
	description = models.TextField(max_length=1000, blank=True)
	price = models.DecimalField(max_digits=5,decimal_places=2, blank=False)
	datereleased = models.DateField(default=date.today)
	timecreated = models.DateTimeField(auto_now_add=True)
	timemodified = models.DateTimeField(auto_now=True)
	collection = models.ForeignKey(Collection, related_name="games", on_delete=models.DO_NOTHING, null=True, blank=True)

	objects = GameManager()

	def __str__(self):
		return str(self.name)

	def collection_name(self):
		return self.collection

	def collection_id(self, gamename):
		return self.objects.get(name=gamename).collection.id




