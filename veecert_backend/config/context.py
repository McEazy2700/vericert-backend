from datetime import timedelta
import jwt
from graphql import GraphQLError
import strawberry
from functools import cached_property
from typing import TYPE_CHECKING, Annotated, Optional
from strawberry.fastapi import BaseContext
from .settings import settings

if TYPE_CHECKING:
    from veecert_backend.apps.users.graphql.types.outputs import ClientType, UserType

LazyClientType = Annotated[
    "ClientType", strawberry.lazy("veecert_backend.apps.users.graphql.types.outputs")
]
LazyUserType = Annotated[
    "UserType", strawberry.lazy("veecert_backend.apps.users.graphql.types.outputs")
]


class Context(BaseContext):
    @cached_property
    async def client(self) -> Optional[LazyClientType]:
        from veecert_backend.apps.users.graphql.types.outputs import ClientType
        from veecert_backend.apps.users.models import ClientPackage

        if not self.request:
            return None

        api_public_key = self.request.headers.get("API_PUBLIC_KEY")
        api_secret_key = self.request.headers.get("API_SECRET_KEY")
        if not api_public_key or not api_secret_key:
            return None
        client_package = await ClientPackage.manager.validate_keys(
            api_public_key, api_secret_key
        )
        return ClientType.from_model(client_package.client)

    @cached_property
    async def user(self) -> Optional[LazyUserType]:
        from veecert_backend.apps.users.graphql.types.outputs import UserType
        from veecert_backend.apps.users.models import User

        if not self.request:
            return None
        authorization = self.request.headers.get("Authorization")
        if not authorization:
            return None
        parts = authorization.split(" ")
        if parts[0] != "Bearer" or len(parts) != 2:
            raise GraphQLError("Invalid Auth Token")
        token = parts[1]
        try:
            payload = jwt.decode(
                token,
                settings.secret_key,
                algorithms=["HS256"],
                leeway=timedelta(seconds=30),
            )
            email = dict(payload).get("email")
            if not email:
                raise GraphQLError("Invalid Auth Token")
            user = await User.manager.one_by_email(email)
            return UserType.from_model(user)
        except jwt.ExpiredSignatureError:
            raise GraphQLError("Signature Expired")


async def get_app_context() -> Context:
    return Context()
