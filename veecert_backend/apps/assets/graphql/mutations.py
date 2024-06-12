from typing import cast
from graphql import GraphQLError
import strawberry

from veecert_backend.apps.assets.graphql.types.outputs import DocumentType
from veecert_backend.apps.users.graphql.types.outputs import UserType
from veecert_backend.config.context import Context
from veecert_backend.apps.assets.graphql.types.inputs import NewDocumentInput


@strawberry.type
class AssetMutations:
    @strawberry.mutation
    async def upload_document(
        self, info: strawberry.Info[Context], args: NewDocumentInput
    ) -> DocumentType:
        from ..models import Document
        from veecert_backend.apps.users.models import Client

        context_client = await info.context.client
        context_user = await info.context.user
        if context_client is None and context_user is None:
            raise GraphQLError("You are not authorized to perform this action")
        client_id = (
            context_client.id
            if context_client is not None
            else (
                await Client.manager.one_by_user_id(cast(UserType, context_user).id)
            ).id
        )
        document = await Document.manager.new(args, int(client_id))
        return DocumentType.from_model(document)
