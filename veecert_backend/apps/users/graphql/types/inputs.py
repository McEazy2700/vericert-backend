from typing import List, Optional
import strawberry

from veecert_backend.apps.common.graphql.scalars import BigInt


@strawberry.input
class EmailPasswordSignUpInput:
    email: str
    password1: str
    password2: str


@strawberry.input
class EmailPasswordSignInInput:
    email: str
    password: str


@strawberry.input
class PurchasePackageInput:
    package_id: BigInt
    txn_in: Optional[str] = None


@strawberry.input
class NewPackageInput:
    name: str
    price: BigInt
    storage_capacity: BigInt
    offers: List[str]
    monthly_requests: BigInt
