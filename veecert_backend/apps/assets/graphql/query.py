from typing import List, Optional
import strawberry

from veecert_backend.apps.assets.graphql.types.inputs import DocumentListOptions
from veecert_backend.apps.assets.graphql.types.outputs import DocumentType


@strawberry.type
class AssetQueries:
    @strawberry.field
    async def documents(
        self, args: Optional[DocumentListOptions] = None
    ) -> List[DocumentType]:
        from ..models import Document

        documents = await Document.manager.filter(args)
        return list(map(lambda item: DocumentType.from_model(item), documents))
