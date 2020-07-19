import graphene
from graphene_django import DjangoObjectType
from django.contrib.auth import get_user_model
from accounts.models import Friendship
from games.models import Game, Collection
from .models import Purchase, MultiPlayerInvite
import django_filters


from graphene_django.filter import DjangoFilterConnectionField


class UserNode(DjangoObjectType):
	class Meta:
		model = get_user_model()
		fields = ('id', 'username', 'email')
		filter_fields = ['username']
		interfaces = (graphene.relay.Node,)

class FriendshipNode(DjangoObjectType):
	class Meta:
		model = Friendship
		fields = ('id', 'user', 'friends')
		filter_fields = ['user__username']
		interfaces = (graphene.relay.Node,)



class GameNode(DjangoObjectType):
	class Meta:
		model = Game
		fields = ('gameid', 'name', 'description', 'price', 'datereleased', 'collection')
		filter_fields = [
			'name',
			'collection__id',
			'collection__collectionname',
			]
		interfaces = (graphene.relay.Node,)

class CollectionNode(DjangoObjectType):
	class Meta:
		model = Collection
		fields = ('id', 'collectionname')
		filter_fields = ['collectionname']
		interfaces = (graphene.relay.Node,)


class PurchaseNode(DjangoObjectType):
	class Meta:
		model = Purchase
		fields = ('user', 'game', 'is_playing', 'has_completed')
		filter_fields = [
			'user__username',
			'game__name',
			'is_playing',
			'has_completed',
			]
		interfaces = (graphene.relay.Node,)


class Query(object):
	pass
	#Player = graphene.relay.Node.Field(UserNode)
	#allPlayers = DjangoFilterConnectionField(UserNode)
	#game = graphene.relay.Node.Field(GameNode)
	#allGames = DjangoFilterConnectionField(GameNode)
	purchase = graphene.relay.Node.Field(PurchaseNode)
	allPurchases = DjangoFilterConnectionField(PurchaseNode)


class addGame(graphene.relay.ClientIDMutation):
	game = graphene.Field(GameNode)

	class Input:
		name = graphene.String()
		price = graphene.Decimal()
		datereleased = graphene.Date()
		collectionname = graphene.String()

	def mutate_and_get_payload(root, info, **input):
		if input.get("collectionname"):
			collection, created = Collection.objects.get_or_create(collectionname=input.get("collectionname"))
			game=Game(name=input.get("name"),
				price=input.get("price"),
				datereleased=input.get("datereleased"),
				collection=collection
				)
		else:
			game=Game(name=input.get("name"),
				price=input.get("price"),
				datereleased=input.get("datereleased"),
				)

		game.save()
		return addGame(game=game)



class addGamePrequels(graphene.relay.ClientIDMutation):
	game = graphene.Field(GameNode)


	class Input:
		gameThatNeedsPrequels = graphene.String()
		name = graphene.String()
		price = graphene.Decimal()
		datereleased = graphene.Date()
		collectionname = graphene.String()

	def mutate_and_get_payload(root, info, gameThatNeedsPrequels=None, **input):
		if gameThatNeedsPrequels:
			temp = Game.objects.get(name=gameThatNeedsPrequels).collection
			if temp:
				collection, created = Collection.objects.get_or_create(collectionname=temp.collectionname)
			else:
				collection, created = Collection.objects.get_or_create(collectionname=input.get("collectionname", "foo"))
		else:
			name = input.get("collectionname", "foo")
			collection, created = Collection.objects.get_or_create(collectionname=name)
		
		game, Gamecreated = Game.objects.get_or_create(
					name=input.get("name"),
					price=input.get("price"),
					datereleased=input.get("datereleased"),
					collection=collection
					)
			
		return addGamePrequels(game=game)


class purchaseGame(graphene.relay.ClientIDMutation):
	purchase = graphene.Field(PurchaseNode)

	class Input:
		userWhoIsPurchasing = graphene.String()
		gameToPurchase = graphene.String()

	def mutate_and_get_payload(root, info, userWhoIsPurchasing=None, gameToPurchase=None):
		if not userWhoIsPurchasing:
			raise Exception("please enter the name of the user")
		if not gameToPurchase:
			raise Exception("Please enter the name of the game you want to purchase")
		u1=get_user_model().objects.get(username=userWhoIsPurchasing)
		g1=Game.objects.get(name=gameToPurchase)
		if u1 and g1:
			purchase, created = Purchase.objects.get_or_create(user=u1, game=g1)
		if created:
			return purchaseGame(purchase=purchase)
		if not created:
			raise Exception("This user already owns this game")



class addFriend(graphene.relay.ClientIDMutation):
	user = graphene.Field(UserNode)

	class Input:
		fromUser = graphene.String(required=True)
		toUser = graphene.String(required=True)

	def mutate_and_get_payload(root, info, fromUser=None, toUser=None):
		if fromUser and toUser:
			u1=get_user_model().objects.get(username=fromUser)
			u2=get_user_model().objects.get(username=toUser)
			friendobj=Friendship.objects.get(user=u1).friends.add(Friendship.objects.get(user=u2))
			
			return addFriend(friendship=friendobj)

class inviteMultiplayer(graphene.Mutation):
	response = graphene.Boolean()

	class Arguments:
		fromUser = graphene.String(required=True)
		toUser = graphene.String(required=True)
		game = graphene.String(required=True)

	def mutate(self, info, fromUser=None, toUser=None, game=None):
		if fromUser and toUser and game:
			if MultiPlayerInvite.objects.invite_to_play_perm(user1=fromUser, user2=toUser, game=game):
				u1=get_user_model().objects.get(username=fromUser)
				u2=get_user_model().objects.get(username=toUser)
				game=Game.objects.get(name=game)
				invite, created = MultiPlayerInvite.objects.get_or_create(invitesender=u1, invitereceiver=u2, game=game)
				if created:
					return inviteMultiplayer(response=True)
				
			return inviteMultiplayer(response=False)



class RelayMutation(graphene.AbstractType):
    addGame = addGame.Field()
    addGamePrequels = addGamePrequels.Field()
    addFriend = addFriend.Field()
    purchaseGame = purchaseGame.Field()

class Mutation(graphene.ObjectType):
    inviteMultiplayer = inviteMultiplayer.Field()
	