from graphql import GraphQLError
import strawberry

from veecert_backend.apps.assets.graphql.types.outputs import DocumentType
from veecert_backend.config.context import Context
from veecert_backend.apps.assets.graphql.types.inputs import NewDocumentInput


@strawberry.type
class AssetMutations:
    @strawberry.mutation
    async def upload_document(self, info: strawberry.Info[Context], args: NewDocumentInput) -> DocumentType:
        from ..models import Document
        client = await info.context.client
        if not client:
            raise GraphQLError("You are not authorized to perform this action")
        document = await Document.manager.new(args, client.id)
        return DocumentType.from_model(document)
