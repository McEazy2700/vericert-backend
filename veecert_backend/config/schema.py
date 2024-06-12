import strawberry

from veecert_backend.apps.assets.graphql.mutations import AssetMutations
from veecert_backend.apps.assets.graphql.query import AssetQueries
from veecert_backend.apps.users.graphql.mutations import UserMutation
from veecert_backend.apps.users.graphql.quereis import UserQueries


@strawberry.type
class VersionQuery:
    @strawberry.field
    def version(self) -> str:
        return "0.0.1"


@strawberry.type
class Query(VersionQuery, AssetQueries, UserQueries):
    pass


@strawberry.type
class Mutation(AssetMutations, UserMutation):
    pass


schema = strawberry.Schema(query=Query, mutation=Mutation)
