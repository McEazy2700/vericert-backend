from graphql import GraphQLError
import strawberry

from veecert_backend.apps.common.contract import Contract
from veecert_backend.apps.users.graphql.types.inputs import (
    EmailPasswordSignUpInput,
    PurchasePackageInput,
)
from veecert_backend.apps.users.graphql.types.outputs import (
    AuthTokenType,
    ClientPackageType,
)
from veecert_backend.config.context import Context


@strawberry.type
class UserMutation:
    @strawberry.mutation
    async def email_password_signup(
        self, args: EmailPasswordSignUpInput
    ) -> AuthTokenType:
        from ..models import User, AuthToken

        user = await User.manager.new_from_email_password(args)
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
