from typing import List
import strawberry
from strawberry.file_uploads import Upload

from veecert_backend.apps.assets.graphql.types.enums import DocumentVisibilityType


@strawberry.input
class NewDocumentInput:
    name: str
    file: Upload
    visibility: DocumentVisibilityType
    authorized_email: List[str]
