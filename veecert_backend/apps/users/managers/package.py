from typing import TYPE_CHECKING

from graphql import GraphQLError
from sqlalchemy import select
from veecert_backend.config.database import async_db_session


if TYPE_CHECKING:
    from ..graphql.types.inputs import NewPackageInput
    from ..models import Package


class PackageManager:
    @classmethod
    async def new(cls, args: "NewPackageInput") -> "Package":
        from ..models import Package

        async with async_db_session() as session:
            package = Package(
                name=args.name,
                price=args.price,
                storage_capacity=args.storage_capacity,
                offers=args.offers,
                monthly_requests=args.monthly_requests,
            )
            session.add(package)
            await session.commit()
            await session.refresh(package)
            return package

    @classmethod
    async def one(cls, package_id: int) -> "Package":
        from ..models import Package

        async with async_db_session() as session:
            result = await session.execute(
                select(Package).where(Package.id == package_id)
            )
            package = result.scalar_one_or_none()
            if package is None:
                raise GraphQLError(f"Package with id {package_id} does not exist")
            return package
