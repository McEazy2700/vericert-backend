from typing import TYPE_CHECKING, List, Optional, Self
import strawberry

from veecert_backend.apps.assets.graphql.types.enums import DocumentVisibilityType
from veecert_backend.apps.common.graphql.scalars import BigInt

if TYPE_CHECKING:
    from ...models import Document, IPFSAsset


@strawberry.type
class IPFSAssetType:
    id: BigInt
    ipfs_hash: str
    pin_size: BigInt
    timestamp: str
    is_duplicate: bool
    client_id: strawberry.Private[Optional[BigInt]] = None

    @strawberry.field
    async def client(self) -> Optional["ClientType"]:
        from veecert_backend.apps.users.models import Client

        if self.client_id:
            client = await Client.manager.one(self.client_id)
            return ClientType.from_model(client)
        return None

    @classmethod
    def from_model(cls, model: "IPFSAsset") -> Self:
        return cls(
            id=model.id,
            ipfs_hash=model.ipfs_hash,
            pin_size=model.pin_size,
            timestamp=model.timestamp,
            is_duplicate=model.is_duplicate,
        )


@strawberry.type
class DocumentType:
    id: BigInt
    name: str
    asset_id: BigInt
    visibility: DocumentVisibilityType
    authorised_email: Optional[List[str]]
    ipfs_asset_id: strawberry.Private[BigInt]
    nft_ipfs_asset_id: strawberry.Private[Optional[BigInt]]

    @strawberry.field
    async def ipfs_asset(self) -> IPFSAssetType:
        from ...models import IPFSAsset

        asset = await IPFSAsset.manager.one(self.ipfs_asset_id)
        return IPFSAssetType.from_model(asset)

    @strawberry.field
    async def nft_ipfs_asset(self) -> Optional[IPFSAssetType]:
        from ...models import IPFSAsset

        if self.nft_ipfs_asset_id:
            asset = await IPFSAsset.manager.one(self.nft_ipfs_asset_id)
            return IPFSAssetType.from_model(asset)
        return None

    @classmethod
    def from_model(cls, model: "Document") -> Self:
        return cls(
            id=model.id,
            name=model.name,
            asset_id=model.asset_id,
            visibility=model.visibility.to_gql(),
            nft_ipfs_asset_id=model.nft_ipfs_asset_id,
            authorised_email=model.authorised_email,
            ipfs_asset_id=model.ipfs_asset_id,
        )


from veecert_backend.apps.users.graphql.types.outputs import ClientType
