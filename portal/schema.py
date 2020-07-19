import graphene
import graphql_jwt
import games.schema
import accounts.schema
import features.schema


class Query(features.schema.Query, games.schema.Query, accounts.schema.Query, graphene.ObjectType):
	pass

class Mutation(games.schema.Mutation, accounts.schema.Mutation, features.schema.Mutation, features.schema.RelayMutation, graphene.ObjectType):
	token_auth = graphql_jwt.ObtainJSONWebToken.Field()
	verify_token = graphql_jwt.Verify.Field()
	refresh_token = graphql_jwt.Refresh.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)