import secrets
from typing import TYPE_CHECKING, Optional

from graphql import GraphQLError
from sqlalchemy import delete, select
from veecert_backend.config.database import async_db_session


if TYPE_CHECKING:
    from ..models import ClientPackage


class ClientPackageManager:
    @classmethod
    async def get_by_client_id(cls, client_id: int) -> Optional["ClientPackage"]:
        from ..models import ClientPackage

        async with async_db_session() as session:
            result = await session.execute(
                select(ClientPackage).where(ClientPackage.client_id == client_id)
            )
            return result.scalar_one_or_none()

    @classmethod
    async def one_by_client_id(cls, client_id: int) -> "ClientPackage":
        from ..models import ClientPackage

        async with async_db_session() as session:
            result = await session.execute(
                select(ClientPackage).where(ClientPackage.client_id == client_id)
            )
            client_package = result.scalar_one_or_none()
            if client_package is None:
                raise GraphQLError("ClientPackage not found")
            return client_package

    @classmethod
    async def new(cls, package_id: int, user_id: int) -> "ClientPackage":
        from ..models import Package, Client, ClientPackage

        client = await Client.manager.get_by_user_id(user_id)
        if client is None:
            client = Client(user_id=user_id)
        package = await Package.manager.one(package_id)

        async with async_db_session() as session:
            await session.execute(
                delete(ClientPackage).where(ClientPackage.client_id == client.id)
            )
            public_key = secrets.token_hex(8)
            private_key = secrets.token_hex(32)
            client_package = ClientPackage(
                api_public_key=public_key,
                api_secret_key=private_key,
                client=client,
                package=package,
            )
            session.add_all([client_package, client])
            await session.commit()
            await session.refresh(client_package)
            return client_package

    @classmethod
    async def validate_keys(cls, public_key: str, private_key: str) -> "ClientPackage":
        from ..models import ClientPackage

        async with async_db_session() as session:
            stmt = select(ClientPackage).where(
                ClientPackage.api_public_key == public_key
            )
            result = await session.execute(stmt)
            client_package = result.scalar_one_or_none()
            if not client_package:
                raise GraphQLError("Invalid API keys")
            if not (client_package.api_secret_key == private_key):
                raise GraphQLError("Invalid API keys")
            return client_package
