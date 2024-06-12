from typing import List
import strawberry

from veecert_backend.apps.users.graphql.types.outputs import PackageType


@strawberry.type
class UserQueries:
    @strawberry.field
    async def packages(self) -> List[PackageType]:
        from ..models import Package

        packages = await Package.manager.all()
        return list(map(lambda item: PackageType.from_model(item), packages))
