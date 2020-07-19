from django.db import models
from django.contrib.auth import get_user_model

from accounts.models import Friendship
from games.models import Game, Collection

import datetime


# Create your models here.



#class PurchaseManager(models.Manager):
#	userqs = Purchase.objects.select_related('user')
#	gameqs = Purchase.objects.select_related('game')
#
#	def games_of(self, user):
#		qs = self.userqs.filter(user=get_user_model().objects.get(username=user.username))
#		return qs
#
#	def has_bought(self, user, game):
#		if user:
#			return bool(self.userqs.filter(user=get_user_model().objects.get(username=user.username)).filter(game=game).exists())
#
#	def has_completed(self, user, game):
#		return bool(Purchase.objects.filter(user=user).filter(game=game).completed)
#
#	def invite_to_play(self, user1, user2, game):
#		user1 = Purchase.objects.filter(user=user1)
#		user2 = Purchase.objects.filter(user=user2)
#		if user1.filter(game=game).is_playing and user2.filter(game=game).exists():
#			Collection.objects.filter(id=Game.objects.filter(game=game).collection)



class Purchase(models.Model):#all purchases class
	user = models.ForeignKey(get_user_model(), blank=False, on_delete=models.CASCADE, related_name="user_purchases")
	game = models.ForeignKey(Game, blank=False, on_delete=models.CASCADE, related_name="purchased_by")
	is_playing = models.BooleanField(default=False)
	has_completed = models.BooleanField(default=False)

	class Meta:
		unique_together = (('user', 'game'),)

	def __str__(self):
		return "{user} purchased {game}".format(user=self.user, game=self.game)

	def completed_status(self):
		return "{status}".format(status=self.has_completed)

	def playing_status(self):
		return "{status}".format(status=self.is_playing)

#	objects = PurchaseManager()

	def games_of(self, user):
		userqs = Purchase.objects.select_related('user')
		gameqs = Purchase.objects.select_related('game')
		qs = self.userqs.filter(user=get_user_model().objects.get(username=user.username))
		return qs







class MultiPlayerInviteManager(models.Manager):
	# get both users, get the game.
	# get all the games in the said game's collection.
	# get all the purchases of both users.
	# check the datereleased delta of the said game with all games in its collection
	# if the delta is positive(ie, certain game is a prequel of said game), continue. else break with error.
	# query certain game from both user's purchases and check if it has been completed, if false, break.

	def invite_to_play_perm(self, user1, user2, game):
		user1 = get_user_model().objects.get(username=user1)
		user2 = get_user_model().objects.get(username=user2)
		game = Game.objects.get(name=game)
		collection_of_game = Collection.objects.get(id=game.collection_id).games.all()
		u1_purchases = user1.user_purchases.all()
		u2_purchases = user2.user_purchases.all()
		gamepqs = game.purchased_by.all()
		if gamepqs.filter(user=user1.id).exists() and gamepqs.filter(user=user2.id).exists():
			if u1_purchases.get(game=game).is_playing:
				for sgame in collection_of_game:
					if (game.datereleased-sgame.datereleased).days>=0:
						if not u1_purchases.get(game=sgame).has_completed and u2_purchases.get(game=sgame).has_completed:
							raise Exception("either of the users has not completed all the prequels.")
						return bool(True)
		return bool(False)













class MultiPlayerInvite(models.Model):
	invitesender = models.ForeignKey(get_user_model(), related_name="invitations_from", on_delete=models.CASCADE) 
	invitereceiver = models.ForeignKey(get_user_model(), related_name="invitations_to", on_delete=models.CASCADE)
	game = models.ForeignKey(Game, related_name="game_invite", on_delete=models.CASCADE)
	timestamp = models.DateTimeField(auto_now_add=True, editable=False)
	


	objects=MultiPlayerInviteManager()
	
	def __str__(self):
		return "{user1} sent a MultiPlayerInvite to {user2} for {game}".format(user1=self.invitesender, user2=self.invitereceiver, game=self.game)

	class Meta:
		unique_together = (('invitesender', 'invitereceiver', 'game'),)

