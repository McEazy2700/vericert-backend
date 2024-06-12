from typing import List, Optional, TypeAlias
import strawberry
from strawberry.file_uploads import Upload

from veecert_backend.apps.assets.graphql.types.enums import DocumentVisibilityType
from veecert_backend.apps.common.graphql.inputs import ListOptions
from veecert_backend.apps.common.graphql.scalars import BigInt


@strawberry.input
class NewDocumentInput:
    name: str
    file: Upload
    visibility: DocumentVisibilityType
    authorized_email: List[str]


@strawberry.input
class DocumentFilter:
    name: Optional[str] = None
    asset_id: Optional[BigInt] = None
    visibility: Optional[DocumentVisibilityType] = None
    client_id: Optional[int] = None


DocumentListOptions: TypeAlias = ListOptions[DocumentFilter, None]
