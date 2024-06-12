from typing import List
import strawberry

from veecert_backend.apps.users.graphql.types.outputs import ClientType, PackageType


@strawberry.type
class UserQueries:
    @strawberry.field
    async def packages(self) -> List[PackageType]:
        from ..models import Package

        packages = await Package.manager.all()
        return list(map(lambda item: PackageType.from_model(item), packages))

    @strawberry.field
    async def user_client(self, user_id: int) -> ClientType:
        from ..models import Client

        client = await Client.manager.one_by_user_id(user_id)
        return ClientType.from_model(client)
