from typing import TYPE_CHECKING, Optional, cast
from fastapi import UploadFile
from graphql import GraphQLError
from sqlalchemy import select
from strawberry.file_uploads import Upload
from veecert_backend.config.database import async_db_session


if TYPE_CHECKING:
    from ..models import IPFSAsset
    from ..utils import PinataMetadata


class IPFSAssetManager:
    @classmethod
    async def get(cls, ipfs_asset_id: int) -> Optional["IPFSAsset"]:
        from ..models import IPFSAsset

        async with async_db_session() as session:
            result = await session.execute(
                select(IPFSAsset).where(IPFSAsset.id == ipfs_asset_id)
            )
            return result.scalar_one_or_none()

    @classmethod
    async def one(cls, ipfs_asset_id: int) -> "IPFSAsset":
        asset = await cls.get(ipfs_asset_id)
        if not asset:
            raise GraphQLError(f"IPFSAsset with id {ipfs_asset_id} does not exist")
        return asset

    @classmethod
    async def new(
        cls,
        file: Upload,
        metadata: Optional["PinataMetadata"] = None,
        client_id: Optional[int] = None,
    ) -> "IPFSAsset":
        from ..utils import Pinata
        from ..models import IPFSAsset
        from veecert_backend.apps.users.models import Client, ClientPackage, Package

        async with async_db_session() as session:
            client: Optional[Client] = None
            upload_file = cast(UploadFile, file)

            if client_id:
                client_package = await ClientPackage.manager.one_by_client_id(client_id)
                package = await Package.manager.one(client_package.package_id)
                client = await Client.manager.one(client_id)
                if (
                    (upload_file.size or 0) + client.used_storage
                ) > package.storage_capacity:
                    raise GraphQLError(
                        f"Insufficient storage on {package.name} tier! Consider an Upgrade."
                    )

            res = await Pinata.pin_file_to_ipfs(file, metadata)

            asset = IPFSAsset(
                ipfs_hash=res.IpfsHash,
                pin_size=res.PinSize,
                timestamp=res.Timestamp,
                is_duplicate=res.isDuplicate,
                client=client,
            )
            if client is not None:
                client.used_storage += res.PinSize
                session.add(client)

            session.add(asset)
            await session.commit()
            await session.refresh(asset)
            return asset
