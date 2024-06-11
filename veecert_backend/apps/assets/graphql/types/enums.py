import enum
from typing import TYPE_CHECKING
import strawberry

if TYPE_CHECKING:
    from ...models import DocumentVisibility


@strawberry.enum
class DocumentVisibilityType(enum.Enum):
    PUBLIC = "PUBLIC"
    PRIVATE = "PRIVATE"

    def to_model_enum(self) -> "DocumentVisibility":
        from ...models import DocumentVisibility

        match self:
            case DocumentVisibilityType.PUBLIC:
                return DocumentVisibility.PUBLIC
            case DocumentVisibilityType.PRIVATE:
                return DocumentVisibility.PRIVATE
