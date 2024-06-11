import strawberry

from veecert_backend.apps.assets.graphql.mutations import AssetMutations
from veecert_backend.apps.users.graphql.mutations import UserMutation


@strawberry.type
class Query:
    @strawberry.field
    def version(self) -> str:
        return "0.0.1"


@strawberry.type
class Mutation(AssetMutations, UserMutation):
    pass


schema = strawberry.Schema(query=Query, mutation=Mutation)
