import graphene
from graphene_django import DjangoObjectType
from django.db.models import Q
#from .models import Profile, FriendRequest
from django.contrib.auth import get_user_model


class UserType(DjangoObjectType):
	class Meta:
		model = get_user_model()
		fields = ('id', 'username', 'email')
		filter_fields = ['username']

class AddPlayer(graphene.Mutation):
	uid = graphene.ID()
	username = graphene.String()
	email = graphene.String()

	class Arguments:
		username = graphene.String(required=True)
		password = graphene.String(required=True)
		email = graphene.String(required=False)

	def mutate(self, info, username, password, **kwargs):
		email = kwargs.get('email', None)
		if email:
			email = {'email': email}
		user = get_user_model()(username=username)
		user.set_password(password)
		user.save()

		return AddPlayer(uid=user.id, username=user.username, email=user.email )

class Mutation(graphene.ObjectType):
	addPlayer = AddPlayer.Field()


class Query(graphene.ObjectType):

	searchPlayer = graphene.List(UserType, username=graphene.String())

	def resolve_searchPlayer(self, info, username=None):
		if username:
			return get_user_model().objects.all().filter(Q(username__icontains=username))


#	me = graphene.Field(UserType)
#	def resolve_me(self, info):
#		user = info.context.user
#		if user.is_anonymous:
#			raise Exception('Not logged in!')
#
#		return user