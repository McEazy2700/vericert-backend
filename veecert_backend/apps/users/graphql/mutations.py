import bcrypt
from typing import Optional
from graphql import GraphQLError
import strawberry

from veecert_backend.config.settings import settings
from veecert_backend.apps.common.contract import Contract
from veecert_backend.apps.users.graphql.types.inputs import (
    EmailPasswordSignInInput,
    EmailPasswordSignUpInput,
    NewPackageInput,
    PurchasePackageInput,
)
from veecert_backend.apps.users.graphql.types.outputs import (
    AuthTokenType,
    ClientPackageType,
    PackageType,
)
from veecert_backend.config.context import Context


@strawberry.type
class UserMutation:
    @strawberry.mutation
    async def new_package(
        self, args: NewPackageInput, super_secret_phrase: Optional[str] = None
    ) -> PackageType:
        from ..models import Package

        if super_secret_phrase is None or (
            super_secret_phrase != settings.super_secret_phrase
        ):
            raise GraphQLError("Failed to perform operation")
        package = await Package.manager.new(args)
        return PackageType.from_model(package)

    @strawberry.mutation
    async def email_password_signup(
        self, args: EmailPasswordSignUpInput
    ) -> AuthTokenType:
        from ..models import User, AuthToken

        user = await User.manager.new_from_email_password(args)
        token = await AuthToken.manager.new(user.email)
        return AuthTokenType.from_model(token)

    @strawberry.mutation
    async def email_password_signin(
        self, args: EmailPasswordSignInInput
    ) -> AuthTokenType:
        from ..models import User, AuthToken

        user = await User.manager.one_by_email(args.email)
        if user.password_hash is None:
            raise GraphQLError("Password Login not found.")
        if not bcrypt.checkpw(args.password.encode(), user.password_hash.encode()):
            raise GraphQLError("Incorrect email or passowrd")
        token = await AuthToken.manager.new(user.email)
        return AuthTokenType.from_model(token)

    @strawberry.mutation
    async def purchase_package(
        self, info: strawberry.Info[Context], args: PurchasePackageInput
    ) -> ClientPackageType:
        from ..models import Package, ClientPackage

        user = await info.context.user
        if user is None:
            raise GraphQLError("You must be authenticated to perform this action")
        package = await Package.manager.one(args.package_id)
        if package.price > 0:
            txn_info = Contract.get_transaction_info(args.txn_in)
            assert (
                txn_info.txn.txn.note == f"Purchase Veecert Package {package.id}"
            ), GraphQLError("Unrecognized Transaction")
            assert txn_info.txn.txn.amt >= package.price, GraphQLError(
                f"Insufficient amount for Package {package.name}"
            )
        client_package = await ClientPackage.manager.new(args.package_id, user.id)
        return ClientPackageType.from_model(client_package)

    @strawberry.mutation
    async def txn_info(self, txn_id: str) -> bool:
        info = Contract.get_transaction_info(txn_id)
        print(info.txn.txn.amt)
        return True
