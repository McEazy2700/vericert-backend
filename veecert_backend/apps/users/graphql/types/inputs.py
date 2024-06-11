import strawberry

from veecert_backend.apps.common.graphql.scalars import BigInt


@strawberry.input
class EmailPasswordSignUpInput:
    email: str
    password1: str
    password2: str


@strawberry.input
class PurchasePackageInput:
    package_id: BigInt
    txn_in: str
