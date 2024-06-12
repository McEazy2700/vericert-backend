import base64
from typing import TYPE_CHECKING, Optional, Sequence

from sqlalchemy import select

from veecert_backend.apps.assets.graphql.types.enums import DocumentVisibilityType
from veecert_backend.apps.common.contract import Contract
from veecert_backend.apps.common.smart_contract_client import NewCertificateNftArgs
from veecert_backend.apps.common.utils.nft_card import generate_nft_image
from veecert_backend.config.database import async_db_session
from veecert_backend.config.settings import settings


if TYPE_CHECKING:
    from ..models import Document
    from ..graphql.types.inputs import NewDocumentInput, DocumentListOptions


def encode_id_to_base64(id: int):
    id_bytes = id.to_bytes((id.bit_length() + 7) // 8, "big")
    base64_bytes = base64.urlsafe_b64encode(id_bytes)
    base64_str = base64_bytes.decode("utf-8")
    return base64_str.rstrip("=")


def decode_base64_to_id(encoded_id: str):
    padding = "=" * (4 - len(encoded_id) % 4)
    encoded_id += padding
    id_bytes = base64.urlsafe_b64decode(encoded_id)
    id = int.from_bytes(id_bytes, "big")
    return id


class DocumentManager:
    @classmethod
    async def filter(
        cls, args: Optional["DocumentListOptions"] = None
    ) -> Sequence["Document"]:
        from ..models import Document, IPFSAsset

        async with async_db_session() as session:
            stmt = select(Document)
            if args:
                if args.filter:
                    if args.filter.name:
                        stmt = stmt.where(Document.name.icontains(args.filter.name))
                    if args.filter.asset_id:
                        stmt = stmt.where(
                            Document.asset_id.icontains(args.filter.asset_id)
                        )
                    if args.filter.visibility:
                        stmt = stmt.where(
                            Document.visibility
                            == args.filter.visibility.to_model_enum()
                        )
                    if args.filter.client_id:
                        stmt = stmt.join(
                            IPFSAsset, Document.ipfs_asset_id == IPFSAsset.id
                        ).where(IPFSAsset.client_id == args.filter.client_id)
                stmt = stmt.limit(args.limit)
                stmt = stmt.offset(args.offset)
            result = await session.execute(stmt)
            return result.scalars().all()

    @classmethod
    async def new(cls, args: "NewDocumentInput", client_id: int) -> "Document":
        from ..models import Document, IPFSAsset
        from ..utils import PinataMetadata
        from veecert_backend.apps.users.models import Client

        async with async_db_session() as session:
            client = await Client.manager.one(client_id)
            keyvalues = {"client_name": client.name, "client_id": client.id}
            metadata = PinataMetadata(name=args.name, keyvalues=keyvalues)
            asset = await IPFSAsset.manager.new(args.file, metadata, client_id)
            document = Document(
                name=args.name,
                visibility=args.visibility.to_model_enum(),
                authorised_email=args.authorized_email,
                ipfs_asset=asset,
            )
            session.add(document)
            await session.commit()
            await session.refresh(document)
            doc_nft_name = (
                f"{f"PB-{document.name}"[:10]}..."
                if len(document.name) > 8
                else f"PB-{document.name}"
            )
            nft_asset = await generate_nft_image(
                document.id,
                doc_nft_name,
                "VEC-PB"
                if args.visibility == DocumentVisibilityType.PUBLIC
                else "VEC-PR",
                f"{settings.frontend_base_url}/explore/{asset.ipfs_hash}",
            )
            encoded_id = encode_id_to_base64(document.id)
            nft_args = NewCertificateNftArgs(
                name=doc_nft_name,
                image_url=f"{settings.pinyata_gateway_url}/hash/{nft_asset.ipfs_hash}",
                certificate_id=document.id,
                metadata_hash=asset.ipfs_hash,
                unit_name=f"B{encoded_id}"
                if args.visibility == DocumentVisibilityType.PUBLIC
                else f"R{encoded_id}",
            )
            result = Contract.get_app_client().create_certificate_nft(args=nft_args)
            asset_id = result.return_value
            document.nft_ipfs_asset = nft_asset
            document.asset_id = asset_id
            session.add(document)
            await session.commit()
            await session.refresh(document)
            return document
