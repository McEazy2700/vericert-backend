from typing import TYPE_CHECKING

from veecert_backend.config.database import async_db_session


if TYPE_CHECKING:
    from ..models import Document
    from ..graphql.types.inputs import NewDocumentInput


class DocumentManager:
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
            return document
