from django.db import models
from django.contrib.auth import get_user_model
from django.dispatch import Signal
from games.models import Game


friendship_accepted = Signal()
friendship_declined = Signal()
friendship_cancelled = Signal()




def create_friendship_instance(sender, instance, created, raw, **kwargs):
	from accounts.models import Friendship
	if created and not raw:
		Friendship.objects.create(user=instance)

# Signal connections
models.signals.post_save.connect(create_friendship_instance,
								sender=get_user_model(),
								dispatch_uid='friends.signals.create_' \
												'friendship_instance')




# Create your models here.

# https://learndjango.com/tutorials/django-best-practices-referencing-user-model

# https://github.com/muhuk/django-simple-friends/tree/v0.5

class FriendshipManager(models.Manager):
	def friends_of(self, user, shuffle=False):
		qs = get_user_model().objects.filter(friendship__friends__user=user)
		if shuffle:
			qs = qs.order_by('?')
		return qs

	def are_friends(self, user1, user2):
		return bool(Friendship.objects.get(user=user1).friends.filter(user=user2).exists())

	def befriend(self, user1, user2):
		if user1 != user2:
			Friendship.objects.get(user=user1).friends.add(Friendship.objects.get(user=user2))
		else:
			print("A user cannot add itself as a friend.")
		# Now that user1 accepted user2's friend request we should delete any
		# request by user1 to user2 so that we don't have ambiguous data
		#Request.objects.filter(from_user=user1, to_user=user2).delete()

	def unfriend(self, user1, user2):
		# Break friendship link between users
		Friendship.objects.get(user=user1).friends.remove(Friendship.objects.get(user=user2))
		# Delete Request's as well
		#Request.objects.filter(from_user=user1, to_user=user2).delete()
		#Request.objects.filter(from_user=user2, to_user=user1).delete()



class Friendship(models.Model):
	user = models.OneToOneField(get_user_model(), related_name='friendship', on_delete=models.CASCADE)
	friends = models.ManyToManyField("self", symmetrical=True, blank=True, related_name="friendship")

	objects = FriendshipManager()

	def __str__(self):
		return "add {user} as a friend".format(user=self.user)


	def friend_count(self):
		return self.friends.count()

































#class Request(models.Model):
#	from_user = models.ForeignKey(get_user_model(), related_name="invitations_from", on_delete=models.CASCADE)
#	to_user = models.ForeignKey(get_user_model(), related_name="invitations_to", on_delete=models.CASCADE)
#	created = models.DateTimeField(auto_now_add=True, editable=False)
#
#	def __str__(self):
#		return "{user1} sent a friend request to {user2}".format(user1=self.from_user, user2=self.to_user)
#
#
#	class Meta:
#		unique_together = (('to_user', 'from_user'),)
#
#
#	def accept(self):
#		Friendship.objects.befriend(self.from_user, self.to_user)
#		self.accepted = True
#		self.save()
#		friendship_accepted.send(sender=self)
#
#	def decline(self):
#		friendship_declined.send(sender=self)
#		self.delete()
#
#	def cancel(self):
#		friendship_cancelled.send(sender=self)
#		self.delete()
#
#
#
#
