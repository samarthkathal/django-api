import graphene
from graphene_django import DjangoObjectType
from django.db.models import Q
import django_filters
from graphene_django.filter import DjangoFilterConnectionField

from .models import Game, Collection


class GameType(DjangoObjectType):
	class Meta:
		model = Game

class CollectionType(DjangoObjectType):
	class Meta:
		model = Collection



#class AddGame(graphene.Mutation):
#	game = graphene.Field(lambda: GameType)
#	
#	class Arguments:
#		name = graphene.String()
#		price = graphene.Decimal()
#		description = graphene.String()
#		groupid = graphene.String()
#		datereleased = graphene.Date()
#		
#	def mutate(self, info, name, price, datereleased, description, **kwargs):
#		groupid = kwargs.get('groupid', None)
#		collection = kwargs.get('collection', None)
#		if groupid:
#			groupid = {'groupid': groupid}
#		game = Game(name=name, price=price, datereleased=datereleased, description=description, **groupid)
#		game.save()
#		response = "name, price, datereleased, description, and maybe a groupid added successfully"
#		return AddGame(game=game)
#
#class UpdateGroupID(graphene.Mutation):
#	game = graphene.Field(lambda: GameType)
#	response = graphene.String()
#
#	class Arguments:
#		gameid = graphene.ID()
#		groupid = graphene.String()
#
#	def mutate(self, info, gameid, groupid):
#		if gameid and groupid:
#			game = Game.objects.get(pk=gameid) 
#			game.groupid = groupid
#			game.save()
#			response = "game has been added to the specified groupid successfully"
#			return AddGame(game=game, response=response)
#
#

class Mutation(graphene.ObjectType):
	pass

#	addGameOrGamePrequels = AddGame.Field()
#	updateGamePrequels = UpdateGroupID.Field()








class Query(graphene.ObjectType):
	allGames = graphene.List(GameType, searchByGameName=graphene.String(), searchByCollectionName=graphene.String())
	searchGame = graphene.List(GameType, name=graphene.String())

	def resolve_searchGame(self, info, name=None):
		if name:
			return Game.objects.all().filter(Q(Name__icontains=name))



	def resolve_allGames(self, info, searchByCollectionName=None, searchByGameName=None, **kwargs):
		qs = Game.objects.all()
		if searchByCollectionName:
			qs = qs.filter(Q(collection=searchByCollectionName))
		if searchByGameName:
			qs = qs.filter(Q(name__icontains=searchByGameName))

		return qs




#	fetchCollectionOfGame = graphene.List(GameType, searchByGameName=graphene.String())
#
#
#	def resolve_fetchCollectionOfGame(self, info, searchByGameName=graphene.String()):
#		if searchByGameName:
#			id = Game.objects.get(name=searchByGameName).collection.id
#			refinedgameqs = Collection.objects.get(id=id).groups.all()
#
#			return refinedgameqs





#	allcollections = graphene.List(CollectionType, searchByCollectionName=graphene.String(), searchByCollectionID=graphene.ID())
#	def resolve_allCollections(self, info, searchByCollectionName=None, searchByCollectionID=None, **kwargs):
#		qs = Game.objects.all()
#		if searchByCollectionName:
#			qs = qs.filter(Q(collectionname__icontains=searchByCollectionName))
#		if searchByCollectionID:
#			qs = qs.filter(Q(id=searchByCollectionID))
#
#		return qs





#class GameNode(DjangoObjectType):
#	class Meta:
#		model = Game
#		interfaces = (graphene.relay.Node, )
#
#
#class CollectionNode(DjangoObjectType):
#	class Meta:
#		model = Collection
#		interfaces = (graphene.relay.Node, )
#
#
#
#class GameFilter(django_filters.FilterSet):
#	class Meta:
#		model = Game
#		fields = {
#			'name': ['icontains'],
#			'price': ['lte', 'gte'],
#		}
#
#class RelayQuery(graphene.ObjectType):
#	relayGame = graphene.relay.Node.Field(GameNode)
#	relayCollection = graphene.relay.Node.Field(GameNode)


