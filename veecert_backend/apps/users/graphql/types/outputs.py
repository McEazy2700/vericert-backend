from typing import TYPE_CHECKING, List, Optional, Self
import strawberry
from veecert_backend.apps.common.graphql.scalars import BigInt
from veecert_backend.apps.users.models import ClientPackage


if TYPE_CHECKING:
    from ...models import Client, User, AuthToken, Package


@strawberry.type
class PackageType:
    id: BigInt
    name: str
    price: BigInt
    offers: List[str]
    storage_capacity: BigInt
    monthly_requests: BigInt

    @classmethod
    def from_model(cls, model: "Package") -> Self:
        return cls(
            id=model.id,
            name=model.name,
            price=model.price,
            offers=model.offers,
            storage_capacity=model.storage_capacity,
            monthly_requests=model.monthly_requests,
        )


@strawberry.type
class ClientPackageType:
    id: int
    client_id: strawberry.Private[int]
    package_id: strawberry.Private[int]
    txn_id: Optional[str] = None
    api_public_key: str
    api_secret_key: str
    has_pending_payment: bool

    @strawberry.field
    async def client(self) -> "ClientType":
        from ...models import Client

        client = await Client.manager.one(self.client_id)
        return ClientType.from_model(client)

    @strawberry.field
    async def package(self) -> "PackageType":
        from ...models import Package

        package = await Package.manager.one(self.package_id)
        return PackageType.from_model(package)

    @classmethod
    def from_model(cls, model: "ClientPackage") -> Self:
        return cls(
            id=model.id,
            txn_id=model.txn_id,
            client_id=model.client_id,
            package_id=model.package_id,
            api_public_key=model.api_public_key,
            api_secret_key=model.api_secret_key,
            has_pending_payment=model.has_pending_payment,
        )


@strawberry.type
class AuthTokenType:
    token: str
    refresh_token: str
    user_id: strawberry.Private[BigInt]

    @strawberry.field
    async def user(self) -> "UserType":
        from ...models import User

        user = await User.manager.one_by_id(self.user_id)
        return UserType.from_model(user)

    @classmethod
    def from_model(cls, model: "AuthToken") -> Self:
        return cls(
            token=model.auth_token, refresh_token=model.id, user_id=model.user_id
        )


@strawberry.type
class ClientType:
    id: int
    name: str
    image_url: Optional[str] = None
    used_storage: int
    user_id: strawberry.Private[int]

    @strawberry.field
    async def user(self) -> "UserType":
        from ...models import User

        user = await User.manager.one_by_id(self.user_id)
        return UserType.from_model(user)

    @classmethod
    def from_model(cls, model: "Client") -> Self:
        return cls(
            id=model.id,
            name=model.name,
            image_url=model.image_url,
            used_storage=model.used_storage,
            user_id=model.user_id,
        )


@strawberry.type
class UserType:
    id: int
    email: str

    @strawberry.field
    async def client(self) -> "ClientType":
        from ...models import Client

        client = await Client.manager.one_by_user_id(self.id)
        return ClientType.from_model(client)

    @classmethod
    def from_model(cls, model: "User") -> Self:
        return cls(id=model.id, email=model.email)
