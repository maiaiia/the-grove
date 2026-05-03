import strawberry

from .resolvers import PlantQuery, PlantMutation
from .auth_resolvers import AuthQuery, AuthMutation

@strawberry.type
class Query(PlantQuery, AuthQuery):
    pass

@strawberry.type
class Mutation(PlantMutation, AuthMutation):
    pass